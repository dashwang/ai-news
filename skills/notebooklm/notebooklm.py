"""
NotebookLM 自动化技能
通过 URL 生成 AI 视频/PPT，并发布到微信公众号
"""

import asyncio
import os
import json
import time
from pathlib import Path
from typing import Optional
from datetime import datetime

try:
    from notebooklm import NotebookLMClient
except ImportError:
    print("请安装 notebooklm-py: pip install notebooklm-py")


OUTPUT_DIR = Path("output/notebooklm")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class NotebookLMPublisher:
    def __init__(self):
        self.client: Optional[NotebookLMClient] = None
        self.current_notebook = None
        self.sources = []

    async def login(self) -> bool:
        """登录 NotebookLM"""
        try:
            self.client = await NotebookLMClient.from_storage()
            print("✅ 已登录 NotebookLM")
            return True
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            return False

    async def create_notebook(self, name: str):
        """创建笔记本"""
        if not self.client:
            await self.login()

        self.current_notebook = await self.client.notebooks.create(name)
        print(f"✅ 创建笔记本: {self.current_notebook.name}")
        return self.current_notebook

    async def add_source(self, source_url: str):
        """添加源"""
        if not self.current_notebook:
            await self.create_notebook(
                f"AI内容_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )

        if not self.client:
            await self.login()

        source = await self.client.sources.add(self.current_notebook, url=source_url)
        self.sources.append(source)
        print(f"✅ 添加源: {source_url}")
        return source

    async def generate_slide_deck(self, wait: bool = True) -> Optional[object]:
        """生成 PPT (Slide Deck)"""
        if not self.current_notebook or not self.client:
            print("❌ 请先创建笔记本并添加源")
            return None

        print("🎨 正在生成 PPT...")
        slides = await self.client.slide_deck.create(
            self.current_notebook, language="zh-CN"
        )

        if wait:
            print("⏳ 等待 PPT 生成完成...")
            slides = await self.client.slide_deck.wait_for_completion(slides)
            print("✅ PPT 生成完成")

        return slides

    async def generate_video(
        self, format: str = "brief", style: str = "auto_select", wait: bool = True
    ) -> Optional[object]:
        """生成视频 (Video Overview)"""
        if not self.current_notebook or not self.client:
            print("❌ 请先创建笔记本并添加源")
            return None

        print("🎬 正在生成视频...")
        video = await self.client.videos.create(
            self.current_notebook,
            format=format,  # brief, explainer
            style=style,  # auto_select, classic, whiteboard, anime, watercolor 等
            language="zh-CN",
        )

        if wait:
            print("⏳ 等待视频生成完成（可能需要几分钟）...")
            video = await self.client.videos.wait_for_completion(video)
            print("✅ 视频生成完成")

        return video

    async def download_slides(self, output_name: str = None) -> Optional[Path]:
        """下载 PPT"""
        if not self.client:
            print("❌ 未连接到 NotebookLM")
            return None

        slides = await self.generate_slide_deck(wait=True)
        if not slides:
            return None

        if output_name is None:
            output_name = (
                f"notebooklm_slides_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )

        output_path = OUTPUT_DIR / f"{output_name}.pptx"

        await self.client.slide_deck.download(slides, str(output_path))
        print(f"✅ PPT 已保存: {output_path}")

        return output_path

    async def download_video(self, output_name: str = None) -> Optional[Path]:
        """下载视频"""
        if not self.client:
            print("❌ 未连接到 NotebookLM")
            return None

        video = await self.generate_video(wait=True)
        if not video:
            return None

        if output_name is None:
            output_name = f"notebooklm_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        output_path = OUTPUT_DIR / f"{output_name}.mp4"

        await self.client.videos.download(video, str(output_path))
        print(f"✅ 视频已保存: {output_path}")

        return output_path

    async def process_url(
        self, url: str, generate_ppt: bool = True, generate_video: bool = False
    ) -> dict:
        """
        处理 URL，生成内容
        返回结果包含文件路径
        """
        result = {
            "url": url,
            "notebook_name": None,
            "ppt_path": None,
            "video_path": None,
            "status": "pending",
        }

        try:
            # 1. 添加源
            await self.add_source(url)
            result["notebook_name"] = self.current_notebook.name

            # 2. 生成 PPT
            if generate_ppt:
                ppt_path = await self.download_slides()
                result["ppt_path"] = str(ppt_path) if ppt_path else None

            # 3. 生成视频（可选）
            if generate_video:
                video_path = await self.download_video()
                result["video_path"] = str(video_path) if video_path else None

            result["status"] = "success"

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            print(f"❌ 处理失败: {e}")

        return result

    async def close(self):
        """关闭连接"""
        if self.client:
            await self.client.close()


async def quick_generate(url: str, output_type: str = "ppt") -> dict:
    """
    快速生成函数
    output_type: "ppt", "video", "both"
    """
    publisher = NotebookLMPublisher()

    try:
        # 登录
        if not await publisher.login():
            return {"status": "error", "error": "登录失败"}

        # 处理
        generate_ppt = output_type in ["ppt", "both"]
        generate_video = output_type in ["video", "both"]

        result = await publisher.process_url(
            url, generate_ppt=generate_ppt, generate_video=generate_video
        )

        return result

    finally:
        await publisher.close()


def generate_from_url(url: str, output_type: str = "ppt") -> dict:
    """同步入口"""
    return asyncio.run(quick_generate(url, output_type))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python notebooklm.py <URL> [ppt|video|both]")
        sys.exit(1)

    url = sys.argv[1]
    output_type = sys.argv[2] if len(sys.argv) > 2 else "ppt"

    print(f"🔄 正在处理: {url}")
    print(f"📦 输出类型: {output_type}")

    result = generate_from_url(url, output_type)
    print("\n📋 结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
