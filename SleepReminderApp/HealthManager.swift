//
//  HealthManager.swift
//  SleepReminder
//
//  读取 Apple Health 数据
//

import Foundation
import HealthKit

class HealthManager: ObservableObject {
    private let healthStore = HKHealthStore()
    
    @Published var sleepScore: Int = 0
    @Published var lastNightSleep: Double = 0.0
    @Published var todayScreenTime: Double = 0.0
    
    // Health Data Types
    private let readTypes: Set<HKObjectType> = {
        var types = Set<HKObjectType>()
        if let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) {
            types.insert(sleepType)
        }
        if let heartType = HKObjectType.quantityType(forIdentifier: .heartRate) {
            types.insert(heartType)
        }
        return types
    }()
    
    func requestAuthorization() {
        guard HKHealthStore.isHealthDataAvailable() else { return }
        
        healthStore.requestAuthorization(toShare: nil, read: readTypes) { success, error in
            if let error = error {
                print("HealthKit Auth Error: \(error.localizedDescription)")
            }
        }
    }
    
    // MARK: - 获取睡眠数据
    func fetchSleepData() {
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else { return }
        
        let predicate = HKQuery.predicateForSamples(
            withStart: Calendar.current.date(byAdding: .hour, value: -24, to: Date()),
            end: Date(),
            options: .strictStartDate
        )
        
        let query = HKSampleQuery(
            sampleType: sleepType,
            predicate: predicate,
            limit: HKObjectQueryNoLimit,
            sortDescriptors: nil
        ) { [weak self] _, samples, error in
            guard let samples = samples as? [HKCategorySample], error == nil else { return }
            
            var totalSleep: Double = 0
            for sample in samples {
                // 只计算睡眠时间（不包括wake）
                if sample.value == HKCategoryValueSleepAnalysis.asleepUnspecified.rawValue ||
                   sample.value == HKCategoryValueSleepAnalysis.asleepCore.rawValue ||
                   sample.value == HKCategoryValueSleepAnalysis.asleepDeep.rawValue ||
                   sample.value == HKCategoryValueSleepAnalysis.asleepREM.rawValue {
                    totalSleep += sample.endDate.timeIntervalSince(sample.startDate) / 3600
                }
            }
            
            DispatchQueue.main.async {
                self?.lastNightSleep = totalSleep
                self?.sleepScore = self?.calculateSleepScore(hours: totalSleep) ?? 0
            }
        }
        
        healthStore.execute(query)
    }
    
    // MARK: - 计算睡眠分数
    private func calculateSleepScore(hours: Double) -> Int {
        // 简单算法：7-9小时为满分100，低于5小时为0
        if hours >= 9 { return 100 }
        if hours >= 7 { return 90 }
        if hours >= 6 { return 75 }
        if hours >= 5 { return 60 }
        if hours >= 4 { return 40 }
        return max(0, Int((hours - 3) * 20))
    }
    
    // MARK: - 获取屏幕时间（需要额外配置）
    func fetchScreenTime() {
        // 注意：Screen Time API 需要额外授权
        // 这里用模拟数据演示
        // 实际实现需要使用 Family Controls 框架
        
        // 模拟数据
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.todayScreenTime = Double.random(in: 4...10)
        }
    }
}
