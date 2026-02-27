//
//  SleepReminderApp.swift
//  SleepReminder
//
//  Created by Pieter Levels on 2026-02-26.
//  Vibe Coding: AI-powered sleep reminder
//

import SwiftUI
import HealthKit
import UserNotifications

@main
struct SleepReminderApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// MARK: - Content View
struct ContentView: View {
    @StateObject private var healthManager = HealthManager()
    @State private var sleepGoal: Int = 8 // hours
    @State private var reminderTime: Date = Date()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Sleep Score Card
                    SleepScoreCard(
                        score: healthManager.sleepScore,
                        hoursSlept: healthManager.lastNightSleep
                    )
                    
                    // Screen Time Card
                    ScreenTimeCard(
                        totalHours: healthManager.todayScreenTime
                    )
                    
                    // Settings Section
                    SettingsSection(
                        sleepGoal: $sleepGoal,
                        reminderTime: $reminderTime
                    )
                    
                    // Quick Actions
                    QuickActionsView()
                }
                .padding()
            }
            .navigationTitle("😴 Sleep Tracker")
            .onAppear {
                healthManager.requestAuthorization()
                healthManager.fetchSleepData()
                healthManager.fetchScreenTime()
            }
        }
    }
}

// MARK: - Sleep Score Card
struct SleepScoreCard: View {
    let score: Int
    let hoursSlept: Double
    
    var scoreColor: Color {
        if score >= 80 { return .green }
        if score >= 60 { return .yellow }
        return .red
    }
    
    var body: some View {
        VStack(spacing: 15) {
            HStack {
                Text("昨晚睡眠")
                    .font(.headline)
                Spacer()
                Text("\(score)分")
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(scoreColor)
            }
            
            ProgressView(value: min(hoursSlept / 12, 1.0))
                .tint(scoreColor)
            
            HStack {
                Image(systemName: "moon.zzz.fill")
                    .foregroundColor(.blue)
                Text("\(String(format: "%.1f", hoursSlept))小时")
                    .font(.title3)
                Spacer()
                Text(sleepQuality)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
    
    var sleepQuality: String {
        if hoursSlept >= 7 { return "✅ 睡眠充足" }
        if hoursSlept >= 6 { return "⚠️ 睡眠不足" }
        return "❌ 严重不足"
    }
}

// MARK: - Screen Time Card
struct ScreenTimeCard: View {
    let totalHours: Double
    
    var body: some View {
        VStack(spacing: 15) {
            HStack {
                Text("今日屏幕时间")
                    .font(.headline)
                Spacer()
                Image(systemName: "iphone")
                    .foregroundColor(.orange)
            }
            
            HStack(alignment: .lastTextBaseline) {
                Text("\(String(format: "%.1f", totalHours))")
                    .font(.system(size: 48, weight: .bold))
                Text("小时")
                    .font(.title3)
                    .foregroundColor(.secondary)
                Spacer()
            }
            
            if totalHours > 6 {
                HStack {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundColor(.red)
                    Text("屏幕时间过长，该休息了！")
                        .font(.caption)
                        .foregroundColor(.red)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Settings Section
struct SettingsSection: View {
    @Binding var sleepGoal: Int
    @Binding var reminderTime: Date
    
    var body: some View {
        VStack(spacing: 15) {
            HStack {
                Text("⚙️ 设置")
                    .font(.headline)
                Spacer()
            }
            
            // Sleep Goal
            HStack {
                Text("目标睡眠时间")
                Spacer()
                Picker("小时", selection: $sleepGoal) {
                    ForEach(5...12, id: \.self) { hour in
                        Text("\(hour)小时").tag(hour)
                    }
                }
                .pickerStyle(.menu)
            }
            
            // Reminder Time
            HStack {
                Text("睡前提醒时间")
                Spacer()
                DatePicker("", selection: $reminderTime, displayedComponents: .hourAndMinute)
                    .labelsHidden()
            }
            
            Button(action: {}) {
                HStack {
                    Image(systemName: "bell.badge")
                    Text("开启睡眠提醒")
                        .fontWeight(.semibold)
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(12)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Quick Actions
struct QuickActionsView: View {
    var body: some View {
        VStack(spacing: 15) {
            HStack {
                Text("⚡ 快捷操作")
                    .font(.headline)
                Spacer()
            }
            
            HStack(spacing: 15) {
                ActionButton(icon: "moon.fill", title: "马上睡觉", color: .indigo)
                ActionButton(icon: "sun.max.fill", title: "起床打卡", color: .orange)
                ActionButton(icon: "chart.bar.fill", title: "周报", color: .green)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

struct ActionButton: View {
    let icon: String
    let title: String
    let color: Color
    
    var body: some View {
        VStack {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            Text(title)
                .font(.caption)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(color.opacity(0.1))
        .cornerRadius(12)
    }
}
