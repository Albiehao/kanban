import Foundation

struct SleepRecoveryCalculator {
    /// 当前版本只使用“时长 + 连续性 + 规律性”三类指标。
    /// 深睡 / REM 仅作为展示和趋势指标，不直接高权重参与评分。
    func score(
        metrics: SleepMetrics,
        recentBedtimes: [Date] = []
    ) -> SleepRecoveryScore {
        let durationScore = scoreDuration(metrics.totalSleep)
        let continuityScore = scoreContinuity(metrics)
        let consistencyScore = scoreConsistency(recentBedtimes)

        let total: Double
        if let consistencyScore {
            total = durationScore * 0.50
                + consistencyScore * 0.30
                + continuityScore * 0.20
        } else {
            // 没有足够历史数据时，将规律性权重按比例重新分配给时长与连续性。
            total = durationScore * (0.50 / 0.70)
                + continuityScore * (0.20 / 0.70)
        }

        return SleepRecoveryScore(
            total: total,
            durationScore: durationScore,
            continuityScore: continuityScore,
            consistencyScore: consistencyScore
        )
    }

    private func scoreDuration(_ totalSleep: TimeInterval) -> Double {
        let hours = totalSleep / 3600

        switch hours {
        case ..<4:
            return max(0, hours / 4 * 35)
        case 4..<6:
            return 35 + (hours - 4) / 2 * 35
        case 6..<7:
            return 70 + (hours - 6) * 20
        case 7...9:
            return 90 + (1 - abs(hours - 8) / 1) * 10
        case 9..<10:
            return 90 - (hours - 9) * 15
        default:
            return max(40, 75 - (hours - 10) * 10)
        }
    }

    private func scoreContinuity(_ metrics: SleepMetrics) -> Double {
        let efficiencyPart = min(max(metrics.sleepEfficiency, 0), 1) * 70

        let awakeningPenalty = min(Double(metrics.awakenings) * 4, 20)
        let awakeMinutes = metrics.awakeTime / 60
        let awakePenalty = min(awakeMinutes / 30 * 10, 10)

        return min(max(efficiencyPart + 30 - awakeningPenalty - awakePenalty, 0), 100)
    }

    private func scoreConsistency(_ bedtimes: [Date]) -> Double? {
        guard bedtimes.count >= 5 else { return nil }

        let calendar = Calendar.current
        let minutes = bedtimes.map { date -> Double in
            let components = calendar.dateComponents([.hour, .minute], from: date)
            var value = Double((components.hour ?? 0) * 60 + (components.minute ?? 0))
            // 将凌晨 0~6 点映射到 24~30 点，避免 23:50 和 00:10 被错误识别为差 23 小时。
            if value < 6 * 60 {
                value += 24 * 60
            }
            return value
        }

        let mean = minutes.reduce(0, +) / Double(minutes.count)
        let variance = minutes.reduce(0) { partial, value in
            let diff = value - mean
            return partial + diff * diff
        } / Double(minutes.count)
        let standardDeviation = sqrt(variance)

        switch standardDeviation {
        case ..<15:
            return 100
        case 15..<30:
            return 90
        case 30..<60:
            return 75
        case 60..<90:
            return 55
        default:
            return max(20, 55 - (standardDeviation - 90) / 3)
        }
    }
}
