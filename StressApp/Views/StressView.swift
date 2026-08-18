import SwiftUI

struct StressView: View {
    @ObservedObject var viewModel: StressViewModel

    var body: some View {
        Group {
            switch viewModel.state {
            case .idle, .loading:
                ProgressView("Reading Health data…")
            case .insufficientData:
                ContentUnavailableView(
                    "Not enough HRV data",
                    systemImage: "heart.text.square",
                    description: Text("At least 8 valid HRV samples are required to build a personal baseline and score the latest reading.")
                )
            case .failed(let message):
                ContentUnavailableView(
                    "Health data unavailable",
                    systemImage: "exclamationmark.triangle",
                    description: Text(message)
                )
            case .loaded(let snapshot):
                ScrollView {
                    VStack(spacing: 24) {
                        Gauge(value: Double(snapshot.stressScore), in: 0...100) {
                            Text("Relative stress")
                        } currentValueLabel: {
                            Text("\(snapshot.stressScore)")
                                .font(.system(size: 42, weight: .bold, design: .rounded))
                        }
                        .gaugeStyle(.accessoryCircularCapacity)
                        .scaleEffect(1.8)
                        .padding(.vertical, 44)

                        VStack(spacing: 12) {
                            metric("Latest HRV", value: String(format: "%.1f ms", snapshot.currentHRV))
                            metric("30-day baseline", value: String(format: "%.1f ms", snapshot.baselineHRV))
                            metric("Z-Score", value: String(format: "%.2f", snapshot.zScore))
                            metric("Samples", value: "\(snapshot.sampleCount)")
                        }

                        Text("This score reflects how your latest HRV differs from your own recent baseline. It is not a medical diagnosis.")
                            .font(.footnote)
                            .foregroundStyle(.secondary)
                    }
                    .padding()
                }
                .refreshable {
                    await viewModel.load()
                }
            }
        }
    }

    private func metric(_ title: String, value: String) -> some View {
        HStack {
            Text(title)
                .foregroundStyle(.secondary)
            Spacer()
            Text(value)
                .fontWeight(.semibold)
        }
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 16))
    }
}
