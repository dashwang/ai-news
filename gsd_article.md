<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 20px; color: #fff; font-weight: bold;">Get Shit Done：那个把「 Vibecoding 」变认真的男人</span>
</p>

<p style="margin: 25px 20px 20px; font-size: 15px; line-height: 1.8; color: #333; text-align: justify;">
2026年的开发圈，有两个极端。<br><br>
一边是铺天盖地的「 AI 编程」宣传——仿佛只要你开口说出产品想法，代码就会自动出现。另一边是无数开发者的吐槽：AI生成的代码看起来像那么回事，但稍微上个规模就散架。<br><br>
这种「描述需求→AI生成→得到一坨垃圾」的循环，有了一个新的名字：Vibecoding。<br><br>
说实话，这个词现在已经快变成贬义词了。<br><br>
但今天要聊的这个人，可能要给Vibecoding正名。
</p>

<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">一个不写代码的开发者</strong>
</p>

<p style="margin: 0 20px 15px; font-size: 14px; color: #333; line-height: 1.8;">
GSD（Get Shit Done）的作者叫TÂCHES。<br><br>
他的自我介绍就很有意思：<b>「我是独立开发者。我不写代码，Claude Code写。」</b><br><br>
这句话要是放在两年前，估计会被喷死。但现在，越来越多的人开始理解这句话的分量。<br><br>
TÂCHES不是没试过别的工具。市面上spec-driven的开发工具并不少——BMAD、Speckit、OpenSpec、Taskmaster……他都试过。<br><br>
但他的感受是：<b>这些工具把简单的事情搞得太复杂了。</b><br><br>
什么冲刺仪式、故事点、利益相关方同步、复盘会议、Jira流程……他直言不讳地说：<b>「我不是一家50人的软件公司。我不想演企业流程。我只是个想把好东西做出来的创作者。」</b><br><br>
这话听着是不是特别熟悉？对，很多独立开发者心里都这么想过，但没人好意思说出来。
</p>

<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">Vibecoding的问题出在哪？</strong>
</p>

<p style="margin: 0 20px 15px; font-size: 14px; color: #333; line-height: 1.8;">
Vibecoding被骂，不是没有原因的。<br><br>
你跟AI说「帮我做一个电商网站」，它确实能给你生成一堆代码。但当你仔细看的时候，会发现：<br><br>
• 代码结构一团糟<br>
• 没有任何错误处理<br>
• 完全没有考虑边界情况<br>
• 变量名乱起<br>
• 根本没有可扩展性可言<br><br>
为什么会这样？因为<b>AI不知道你到底想要什么。</b><br><br>
你只给了它一个模糊的需求，它也只能给你一个模糊的结果。这就像你跟设计师说「帮我做个好看logo」，然后怪设计师没读心术。<br><br>
TÂCHES的洞察是：<b>问题的本质是上下文管理。</b><br><br>
当你用AI编程时，随着对话的进行，上下文窗口会越来越满。然后，AI就开始「降智」——它开始遗忘之前说过的话，开始做重复的事情，开始写出质量越来越差的代码。<br><br>
这个问题有一个名字：<b>context rot（上下文腐烂）</b>。
</p>

<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">GSD是怎么解决问题的？</strong>
</p>

<p style="margin: 0 20px 15px; font-size: 14px; color: #333; line-height: 1.8;">
GSD的核心思路其实很简单：<b>复杂性放在系统里，不放在工作流里。</b><br><br>
你作为使用者，只需要记住几个命令：<br><br>
<b>/gsd:new-project</b> — 告诉AI你想做什么。它会一直追问，直到彻底理解你的想法。包括你的目标、约束条件、技术偏好、甚至边界情况。<br><br>
<b>/gsd:discuss-phase</b> — 在正式开发之前，先讨论实现细节。比如你想要什么样的交互方式？API返回什么格式？错误怎么处理？<br><br>
<b>/gsd:plan-phase</b> — AI会基于前面的信息，制定详细的执行计划。这个计划会分成小的「wave」，每个wave里的任务可以并行执行。<br><br>
<b>/gsd:execute-phase</b> — 开始执行。每个任务用全新的上下文窗口，单独提交代码。<br><br>
听起来好像也不复杂？对，<b>这就是重点——复杂性都在系统后台处理，用户体验非常简单。</b>
</p>

<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">为什么它真的有效？</strong>
</p>

<p style="margin: 0 20px 15px; font-size: 14px; color: #333; line-height: 1.8;">
我仔细研究了GSD的设计，有几个点确实很聪明：<br><br>
<b>1. 强制思考</b><br>
在写代码之前，系统会逼你把需求想清楚。你说不清楚？没关系，它会一直问到你说不出来为止。这种「追问式需求分析」，其实是把Agile的「早失败早迭代」理念反过来了——<b>在写代码之前就把问题想清楚，而不是写完之后再改。</b><br><br>
<b>2. 上下文隔离</b><br>
每个任务执行时，AI都使用全新的上下文窗口。20万token，全部用来实现当前任务，零历史垃圾。这就从根本上解决了context rot的问题。<br><br>
<b>3. 原子化提交</b><br>
每个任务完成后单独提交git。这带来的好处是：你随时可以回滚到任何一个版本，不会出现「改了A功能把B功能搞崩了」的情况。<br><br>
<b>4. 验证机制</b><br>
代码写完之后，系统会自动对照最初的需求检查：真的实现了承诺的功能吗？这解决了「AI自说自话」的问题。
</p>

<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">谁在用GSD？</strong>
</p>

<p style="margin: 0 20px 15px; font-size: 14px; color: #333; line-height: 1.8;">
官方说「已被Amazon、Google、Shopify和Webflow的工程师采用」。<br><br>
真实性不好判断，但GitHub上确实收获了不少好评：<br><br>
<i>「只要你清楚自己想要什么，它就真的能给你做出来。不扯淡。」</i><br><br>
<i>「我试过SpecKit、OpenSpec和Taskmaster，这套东西目前给我的结果最好。」</i><br><br>
<i>「这是我给Claude Code加过最强的增强。没有过度设计，是真的把事做完。」</i><br><br>
这些评价里出现最多的词是：<b>「有效」「不扯淡」「真的做完」</b>。<br><br>
看来，GSD精准地击中了一批人的需求：<b>那些受够了复杂流程、只想安静写代码的开发者。</b>
</p>

<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">GSD vs 传统开发</strong>
</p>

<p style="margin: 0 20px 15px; font-size: 14px; color: #333; line-height: 1.8;">
GSD并没有取代传统开发的意思。它的定位很清楚：<b>适合个人开发者或小团队，适合快速验证MVP。</b><br><br>
如果你在做一个50人团队的企业级系统，该用Scrum还得用Scrum。但如果你只是一个人想把想法变成产品，GSD可能是目前最务实的选择。<br><br>
有意思的是，TÂCHES在文档里直接说：<b>「运行Claude Code时建议使用 --dangerously-skip-permissions」</b><br><br>
这句话翻译成人话就是：别让权限确认打断你的flow。创建50个文件，你要确认50次？那这工具干脆别用了。<br><br>
这是一种很极客的价值观：<b>工具应该适应人，而不是让人适应工具。</b>
</p>

<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">写在最后</strong>
</p>

<p style="margin: 0 20px 15px; font-size: 14px; color: #333; line-height: 1.8;">
GSD让我想起了一句话：<b>最好的工具是让你忘记工具存在的工具。</b><br><br>
TÂCHES没有做什么惊天动地的创新。他只是把AI编程领域几个公认的问题——上下文腐烂、需求不清晰、代码质量不稳定——一个一个解决掉。<br><br>
然后用几个简单的命令包装起来。<br><br>
复杂性在系统里，不在工作流里。这句话说起来容易，做起来需要大量的思考和打磨。<br><br>
GSD目前支持Claude Code、OpenCode、Gemini CLI、Codex、Copilot和Antigravity。安装也很简单：<br><br>
<pre style="background: #f5f5f5; padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 13px;">px get-shit-done-cc@latest</pre><br><br>
感兴趣的朋友可以试试。毕竟，<b>管它黑猫白猫，能把shit做完的就是好猫。</b>
</p>

<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">
    👍 觉得有用？不妨分享给朋友 👏
  </span>
</p>

<p style="text-align: center; margin-top: 20px;">
  <img src="https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png" 
       style="width: 180px; height: 180px; border-radius: 8px;" 
       alt="grepAI公众号">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
  📱 扫码关注「grepAI」<br>
  每天早上8点自动送达
</p>

<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">
  💬 欢迎评论交流，说说你的看法
</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">
  © 2026 grepAI | 认真做内容
</p>