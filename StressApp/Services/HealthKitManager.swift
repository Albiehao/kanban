import Foundation
import HealthKit

actor HealthKitManager {
    static let shared = HealthKitManager()

    private let store = HKHealthStore()

    enum HealthKitError: Error {
        case unavailable
        case hrvTypeUnavailable
    }

    func requestAuthorization() async throws {
        guard HKHealthStore.isHealthDataAvailable() else {
            throw HealthKitError.unavailable
        }
        guard let hrvType = HKObjectType.quantityType(forIdentifier: .heartRateVariabilitySDNN) else {
            throw HealthKitError.hrvTypeUnavailable
        }
        try await store.requestAuthorization(toShare: [], read: [hrvType])
    }

    func fetchHRVSamples(days: Int = 30) async throws -> [HRVSample] {
        guard let hrvType = HKObjectType.quantityType(forIdentifier: .heartRateVariabilitySDNN) else {
            throw HealthKitError.hrvTypeUnavailable
        }

        let end = Date()
        let start = Calendar.current.date(byAdding: .day, value: -days, to: end) ?? end
        let predicate = HKQuery.predicateForSamples(withStart: start, end: end)
        let descriptor = HKSampleQueryDescriptor(
            predicates: [.quantitySample(type: hrvType, predicate: predicate)],
            sortDescriptors: [SortDescriptor(\.startDate, order: .forward)]
        )

        let samples = try await descriptor.result(for: store)
        let unit = HKUnit.secondUnit(with: .milli)

        return samples.map {
            HRVSample(date: $0.startDate, sdnnMilliseconds: $0.quantity.doubleValue(for: unit))
        }
        .filter { $0.sdnnMilliseconds > 0 && $0.sdnnMilliseconds.isFinite }
    }
}
