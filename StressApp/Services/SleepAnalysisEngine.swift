import Foundation

struct SleepAnalysisEngine {
    /// 对同一来源、同一阶段、存在重叠或紧邻的区间做合并，避免重复累计时长。
    func normalize(_ segments: [SleepSegment]) -> [SleepSegment] {
        let valid = segments
            .filter { $0.endDate > $0.startDate }
            .sorted {
                if $0.startDate == $1.startDate {
                    return $0.endDate < $1.endDate
                }
                return $0.startDate < $1.startDate
            }

        var result: [SleepSegment] = []

        for segment in valid {
            guard let last = result.last else {
                result.append(segment)
                continue
            }

            let canMerge = last.stage == segment.stage
                && last.sourceName == segment.sourceName
                && segment.startDate <= last.endDate.addingTimeInterval(30)

            if canMerge {
                result.removeLast()
                result.append(
                    SleepSegment(
                        id: last.id,
                        startDate: min(last.startDate, segment.startDate),
                        endDate: max(last.endDate, segment.endDate),
                        stage: last.stage,
                        sourceName: last.sourceName
                    )
                )
            } else {
                result.append(segment)
            }
        }

        return result
    }

    /// 按睡眠片段时间轴切成一晚一晚的 session。
    /// 两段睡眠间隔超过 3 小时，视为新的睡眠会话。
    func makeSessions(from segments: [SleepSegment]) -> [SleepSession] {
        let normalized = normalize(segments)
        guard !normalized.isEmpty else { return [] }

        let sorted = normalized.sorted { $0.startDate < $1.startDate }
        var sessions: [SleepSession] = []
        var bucket: [SleepSegment] = []

        func flush() {
            guard let first = bucket.first, let last = bucket.last else { return }
            sessions.append(
                SleepSession(
                    startDate: first.startDate,
                    endDate: last.endDate,
                    segments: bucket
                )
            )
            bucket.removeAll(keepingCapacity: true)
        }

        for segment in sorted {
            guard let previous = bucket.last else {
                bucket.append(segment)
                continue
            }

            if segment.startDate.timeIntervalSince(previous.endDate) > 3 * 3600 {
                flush()
            }
            bucket.append(segment)
        }

        flush()
        return sessions
    }

    func metrics(for session: SleepSession) -> SleepMetrics {
        let segments = session.segments.sorted { $0.startDate < $1.startDate }

        var totalSleep: TimeInterval = 0
        var awake: TimeInterval = 0
        var core: TimeInterval = 0
        var deep: TimeInterval = 0
        var rem: TimeInterval = 0
        var unspecified: TimeInterval = 0
        var awakenings = 0
        var longestContinuousSleep: TimeInterval = 0
        var currentContinuousSleep: TimeInterval = 0
        var previousWasAsleep = false

        for segment in segments {
            let duration = segment.duration

            switch segment.stage {
            case .awake:
                awake += duration
                if previousWasAsleep {
                    awakenings += 1
                }
                longestContinuousSleep = max(longestContinuousSleep, currentContinuousSleep)
                currentContinuousSleep = 0
                previousWasAsleep = false

            case .core:
                core += duration
                totalSleep += duration
                currentContinuousSleep += duration
                previousWasAsleep = true

            case .deep:
                deep += duration
                totalSleep += duration
                currentContinuousSleep += duration
                previousWasAsleep = true

            case .rem:
                rem += duration
                totalSleep += duration
                currentContinuousSleep += duration
                previousWasAsleep = true

            case .asleepUnspecified:
                unspecified += duration
                totalSleep += duration
                currentContinuousSleep += duration
                previousWasAsleep = true

            case .inBed:
                break
            }
        }

        longestContinuousSleep = max(longestContinuousSleep, currentContinuousSleep)

        let sessionDuration = max(0, session.endDate.timeIntervalSince(session.startDate))
        let efficiency = sessionDuration > 0 ? min(max(totalSleep / sessionDuration, 0), 1) : 0

        return SleepMetrics(
            sessionStart: session.startDate,
            sessionEnd: session.endDate,
            totalSleep: totalSleep,
            awakeTime: awake,
            coreSleep: core,
            deepSleep: deep,
            remSleep: rem,
            unspecifiedSleep: unspecified,
            awakenings: awakenings,
            longestContinuousSleep: longestContinuousSleep,
            sleepEfficiency: efficiency
        )
    }
}
