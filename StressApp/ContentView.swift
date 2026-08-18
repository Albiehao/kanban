import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = StressViewModel()

    var body: some View {
        NavigationStack {
            StressView(viewModel: viewModel)
                .navigationTitle("Stress")
        }
        .task {
            await viewModel.load()
        }
    }
}
