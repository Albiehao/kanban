import Foundation

@MainActor
final class StressViewModel: ObservableObject {
    enum State {
        case idle
        case loading
        case loaded(StressSnapshot)
        case insufficientData
        case failed(String)
    }

    @Published private(set) var state: State = .idle

    private let healthKit = HealthKitManager.shared

    func load() async {
        state = .loading

        do {
            try await healthKit.requestAuthorization()
            let samples = try await healthKit.fetchHRVSamples(days: 30)
            let snapshot = try HRVStressCalculator.calculate(from: samples)
            state = .loaded(snapshot)
        } catch HRVStressCalculator.CalculationError.insufficientData {
            state = .insufficientData
        } catch {
            state = .failed(error.localizedDescription)
        }
    }
}
