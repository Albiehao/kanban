import Foundation
import HealthKit

actor HealthKitManager {
    static let shared = HealthKitManager()

    private let store = HKHealthStore()

    enum HealthKitError: Error {
        case unavailable
        case hrvTypeUnavailable
        case sleepTypeUnavailable
    }

    func requestAuthorization() async throws {
        guard HKHealthStore.isHealthDataAvailable() else {
            throw HealthKitError.unavailable
        }
        guard let hrvType = HKObjectType.quantityType(forIdentifier: .heartRateVariabilitySDNN) else {
            throw HealthKitError.hrvTypeUnavailable
        }
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else {
            throw HealthKitError.sleepTypeUnavailable
        }

        try await store.requestAuthorization(toShare: [], read: [hrvType, sleepType])
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

    func fetchSleepSegments(days: Int = 14) async throws -> [SleepSegment] {
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else {
            throw HealthKitError.sleepTypeUnavailable
        }

        let end = Date()
        let start = Calendar.current.date(byAdding: .day, value: -days, to: end) ?? end
        let predicate = HKQuery.predicateForSamples(withStart: start, end: end)
        let descriptor = HKSampleQueryDescriptor(
            predicates: [.categorySample(type: sleepType, predicate: predicate)],
            sortDescriptors: [SortDescriptor(\.startDate, order: .forward)]
        )

        let samples = try await descriptor.result(for: store)

        return samples.compactMap { sample in
            guard let stage = mapSleepStage(sample.value) else { return nil }
            return SleepSegment(
                startDate: sample.startDate,
                endDate: sample.endDate,
                stage: stage,
                sourceName: sample.sourceRevision.source.name
            )
        }
        .filter { $0.duration > 0 }
    }

    private func mapSleepStage(_ rawValue: Int) -> SleepStage? {
        guard let value = HKCategoryValueSleepAnalysis(rawValue: rawValue) else {
            return nil
        }

        switch value {
        case .inBed:
            return .inBed
        case .awake:
            return .awake
        case .asleepUnspecified:
            return .asleepUnspecified
        case .asleepCore:
            return .core
        case .asleepDeep:
            return .deep
        case .asleepREM:
            return .rem
        @unknown default:
            return nil
        }
    }
}
