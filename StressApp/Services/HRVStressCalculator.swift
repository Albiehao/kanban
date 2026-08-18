import Foundation

enum HRVStressCalculator {
    enum CalculationError: Error {
        case insufficientData
    }

    static func calculate(from samples: [HRVSample], minimumBaselineSamples: Int = 7) throws -> StressSnapshot {
        let sorted = samples
            .filter { $0.sdnnMilliseconds > 0 && $0.sdnnMilliseconds.isFinite }
            .sorted { $0.date < $1.date }

        guard sorted.count >= minimumBaselineSamples + 1,
              let current = sorted.last else {
            throw CalculationError.insufficientData
        }

        let baselineSamples = Array(sorted.dropLast())
        let logged = baselineSamples.map { log($0.sdnnMilliseconds) }
        let currentLogged = log(current.sdnnMilliseconds)

        let mean = logged.reduce(0, +) / Double(logged.count)
        let variance = logged.reduce(0) { partial, value in
            partial + pow(value - mean, 2)
        } / Double(max(logged.count - 1, 1))
        let standardDeviation = sqrt(variance)

        let zScore = standardDeviation > 0 ? (currentLogged - mean) / standardDeviation : 0

        // Lower-than-baseline HRV increases the relative stress score.
        // z = 0 maps to 50. About -2 SD maps near 90 and +2 SD maps near 10.
        let rawScore = 50 - (zScore * 20)
        let stressScore = Int(rawScore.rounded().clamped(to: 0...100))
        let baselineHRV = exp(mean)

        return StressSnapshot(
            currentHRV: current.sdnnMilliseconds,
            baselineHRV: baselineHRV,
            zScore: zScore,
            stressScore: stressScore,
            sampleCount: sorted.count
        )
    }
}

private extension Double {
    func clamped(to range: ClosedRange<Double>) -> Double {
        min(max(self, range.lowerBound), range.upperBound)
    }
}
