import Foundation

struct HRVSample: Sendable, Identifiable {
    let id = UUID()
    let date: Date
    let sdnnMilliseconds: Double
}

struct StressSnapshot: Sendable {
    let currentHRV: Double
    let baselineHRV: Double
    let zScore: Double
    let stressScore: Int
    let sampleCount: Int
}
