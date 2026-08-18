import Foundation

/// App 内部统一的睡眠阶段，避免业务层直接依赖 HealthKit 原始枚举。
enum SleepStage: String, Codable, Sendable, CaseIterable {
    case inBed
    case awake
    case asleepUnspecified
    case core
    case deep
    case rem

    var isAsleep: Bool {
        switch self {
        case .asleepUnspecified, .core, .deep, .rem:
            return true
        case .inBed, .awake:
            return false
        }
    }
}

struct SleepSegment: Identifiable, Codable, Sendable, Equatable {
    let id: UUID
    let startDate: Date
    let endDate: Date
    let stage: SleepStage
    let sourceName: String

    init(
        id: UUID = UUID(),
        startDate: Date,
        endDate: Date,
        stage: SleepStage,
        sourceName: String
    ) {
        self.id = id
        self.startDate = startDate
        self.endDate = endDate
        self.stage = stage
        self.sourceName = sourceName
    }

    var duration: TimeInterval {
        max(0, endDate.timeIntervalSince(startDate))
    }
}

struct SleepSession: Identifiable, Codable, Sendable, Equatable {
    let id: UUID
    let startDate: Date
    let endDate: Date
    let segments: [SleepSegment]

    init(id: UUID = UUID(), startDate: Date, endDate: Date, segments: [SleepSegment]) {
        self.id = id
        self.startDate = startDate
        self.endDate = endDate
        self.segments = segments
    }
}

struct SleepMetrics: Codable, Sendable, Equatable {
    let sessionStart: Date
    let sessionEnd: Date
    let totalSleep: TimeInterval
    let awakeTime: TimeInterval
    let coreSleep: TimeInterval
    let deepSleep: TimeInterval
    let remSleep: TimeInterval
    let unspecifiedSleep: TimeInterval
    let awakenings: Int
    let longestContinuousSleep: TimeInterval
    let sleepEfficiency: Double

    var totalSessionDuration: TimeInterval {
        max(0, sessionEnd.timeIntervalSince(sessionStart))
    }

    var deepRatio: Double {
        guard totalSleep > 0 else { return 0 }
        return deepSleep / totalSleep
    }

    var remRatio: Double {
        guard totalSleep > 0 else { return 0 }
        return remSleep / totalSleep
    }
}

struct SleepRecoveryScore: Codable, Sendable, Equatable {
    let total: Double
    let durationScore: Double
    let continuityScore: Double
    let consistencyScore: Double?

    init(total: Double, durationScore: Double, continuityScore: Double, consistencyScore: Double?) {
        self.total = min(max(total, 0), 100)
        self.durationScore = min(max(durationScore, 0), 100)
        self.continuityScore = min(max(continuityScore, 0), 100)
        self.consistencyScore = consistencyScore.map { min(max($0, 0), 100) }
    }
}
