import Foundation

struct SleepDataService {
    private let healthKit: HealthKitManager
    private let analysisEngine = SleepAnalysisEngine()
    private let recoveryCalculator = SleepRecoveryCalculator()

    init(healthKit: HealthKitManager = .shared) {
        self.healthKit = healthKit
    }

    struct NightAnalysis: Sendable, Equatable {
        let session: SleepSession
        let metrics: SleepMetrics
        let recovery: SleepRecoveryScore
    }

    func loadRecentNights(days: Int = 14) async throws -> [NightAnalysis] {
        let rawSegments = try await healthKit.fetchSleepSegments(days: days)
        let selectedSegments = selectPreferredSource(from: rawSegments)
        let sessions = analysisEngine.makeSessions(from: selectedSegments)
            .filter { session in
                session.segments.contains { $0.stage.isAsleep }
            }

        let bedtimes = sessions.map(\.startDate)

        return sessions.map { session in
            let metrics = analysisEngine.metrics(for: session)
            let historicalBedtimes = bedtimes.filter { $0 < session.startDate }
            let recent = Array(historicalBedtimes.suffix(13))
            let score = recoveryCalculator.score(metrics: metrics, recentBedtimes: recent)

            return NightAnalysis(
                session: session,
                metrics: metrics,
                recovery: score
            )
        }
    }

    /// HealthKit 允许多个来源同时写入睡眠数据。
    /// 第一版先选择“有效睡眠阶段覆盖时长最长”的主要来源，避免跨来源重复累计。
    /// 后续可升级为按每一晚动态选择来源。
    private func selectPreferredSource(from segments: [SleepSegment]) -> [SleepSegment] {
        guard !segments.isEmpty else { return [] }

        let grouped = Dictionary(grouping: segments, by: \.sourceName)

        let ranked = grouped.map { source, items -> (String, TimeInterval, Int) in
            let asleepDuration = items
                .filter { $0.stage.isAsleep }
                .reduce(0) { $0 + $1.duration }

            let stagedCount = items.filter {
                $0.stage == .core || $0.stage == .deep || $0.stage == .rem
            }.count

            return (source, asleepDuration, stagedCount)
        }
        .sorted {
            if $0.2 == $1.2 {
                return $0.1 > $1.1
            }
            return $0.2 > $1.2
        }

        guard let preferredSource = ranked.first?.0 else {
            return segments
        }

        return grouped[preferredSource] ?? segments
    }
}
