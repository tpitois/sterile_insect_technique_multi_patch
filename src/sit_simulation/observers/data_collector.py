import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from sit_simulation.core.constants import StateNames
from sit_simulation.core.simulation import Simulation
from sit_simulation.observers.base_observer import SimulationObserver


class DataCollector(SimulationObserver):
    def __init__(self, output_filepath) -> None:
        self.insects_data = []
        self.output_filepath = output_filepath

    def update(self, simulation: Simulation) -> None:
        for patch in range(simulation.simulation_config.numbers_of_patches):
            row = dict(
                simulation.spatial_manager.numbers_of_insects[patch],
                Day=simulation.current_day
            )
            self.insects_data[patch].loc[simulation.current_day] = row

    def on_exit(self, simulation: Simulation) -> None:
        os.makedirs(self.output_filepath, exist_ok=True)

        self._drop_dead_insects()
        self._replace_nan_with_zero()
        self._create_csv_files()
        self._create_pdf_plots()

    def on_enter(self, simulation: Simulation) -> None:
        self.insects_data = [
            pd.DataFrame(columns=['Day'] + [s.value for s in StateNames])
            for _ in range(simulation.simulation_config.numbers_of_patches)
        ]
        self.update(simulation)

    def _replace_nan_with_zero(self):
        for df in self.insects_data:
            if not df.empty:
                numeric_columns = [col for col in df.columns if col != 'Day']
                df[numeric_columns] = df[numeric_columns].fillna(0)

    def _create_csv_files(self):
        """Create CSV files for each patch's data"""
        for patch_idx, df in enumerate(self.insects_data):
            csv_filename = f"patch_{patch_idx}.csv"
            csv_path = os.path.join(self.output_filepath, csv_filename)
            df.to_csv(csv_path, index=False)

    def _create_pdf_plots(self):
        """Create PDF with subplots for each patch showing insect states over time"""

        pdf_path = os.path.join(self.output_filepath, "insects_analysis.pdf")

        with PdfPages(pdf_path) as pdf:
            # Define colors for each state using ggplot-like colors
            colors = ['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD',
                      '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF',
                      '#AEC7E8', '#FFBB78', '#98DF8A', '#FF9896', '#C5B0D5']

            # Calculate grid dimensions for subplots
            n_patches = len(self.insects_data)
            n_cols = min(3, n_patches)  # Max 3 columns
            n_rows = (n_patches + n_cols - 1) // n_cols

            # Create figure with subplots - adjust size for shared legend
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            fig.suptitle('Insect Population Dynamics by Patch', fontsize=16, fontweight='bold')

            # Handle single subplot case
            if n_patches == 1:
                axes = [axes]
            elif n_patches > 1:
                axes = axes.flatten()

            # Get state names for legend
            states = [s.value for s in StateNames if s != StateNames.DEAD]

            # Plot data for each patch
            lines = []  # To store line objects for legend
            labels = []  # To store labels for legend

            for patch_idx, df in enumerate(self.insects_data):
                ax = axes[patch_idx]

                if df.empty:
                    ax.text(0.5, 0.5, f'Patch {patch_idx}\nNo Data',
                            ha='center', va='center', transform=ax.transAxes,
                            fontsize=12)
                    ax.set_title(f'Patch {patch_idx}', fontweight='bold')
                    continue

                # Plot each state as a separate line
                for state_idx, state in enumerate(states):
                    if state in df.columns and state_idx < len(colors):
                        line = ax.plot(df['Day'], df[state],
                                       color=colors[state_idx],
                                       linewidth=2.5,
                                       alpha=0.8)[0]

                        # Store first occurrence of each line for legend
                        if patch_idx == 0 and state not in labels:
                            lines.append(line)
                            labels.append(state)

                ax.set_title(f'Patch {patch_idx}', fontweight='bold', fontsize=12)
                ax.set_xlabel('Day', fontsize=10)
                ax.set_ylabel('Number of Insects', fontsize=10)
                ax.grid(True, alpha=0.4)

                # Set y-axis to start from 0
                ax.set_ylim(bottom=0, top=10000)

                # Improve tick labels
                ax.tick_params(axis='both', which='major', labelsize=9)

            # Hide empty subplots if any
            for idx in range(len(self.insects_data), len(axes)):
                axes[idx].set_visible(False)

            # Create shared legend at the bottom of the figure
            if lines and labels:
                fig.legend(lines, labels,
                           loc='lower center',
                           bbox_to_anchor=(0.5, 0.02),
                           ncol=min(4, len(labels)),
                           fontsize=10,
                           frameon=True,
                           fancybox=True,
                           shadow=True,
                           framealpha=0.9)

            # Adjust layout to make space for the legend
            plt.tight_layout(rect=(0, 0.05, 1, 0.95))
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()

            # Create summary statistics page
            self._create_summary_page(pdf)

    def _create_summary_page(self, pdf):
        """Create a summary page with overall statistics"""
        # Apply ggplot style for summary page too
        plt.style.use('ggplot')

        fig, ax = plt.subplots(figsize=(12, 8))

        # Hide axes for text page
        ax.axis('off')

        summary_text = "Insect Population Simulation Summary\n\n"
        summary_text += f"Total Patches: {len(self.insects_data)}\n\n"

        total_days = 0
        patches_with_data = 0

        for patch_idx, df in enumerate(self.insects_data):
            if not df.empty:
                patches_with_data += 1
                total_days = max(total_days, len(df))

                summary_text += f"Patch {patch_idx}:\n"
                summary_text += f"  - Simulation Days: {len(df)}\n"
                summary_text += f"  - Date Range: Day {df['Day'].min()} to Day {df['Day'].max()}\n"

                # Add max population for each state
                states = [s.value for s in StateNames]
                for state in states:
                    if state in df.columns:
                        max_pop = df[state].max()
                        final_pop = df[state].iloc[-1] if len(df) > 0 else 0
                        summary_text += f"  - {state}: Max={max_pop:.0f}, Final={final_pop:.0f}\n"
                summary_text += "\n"

        # Add overall summary
        summary_text += f"\nOverall Summary:\n"
        summary_text += f"  - Patches with data: {patches_with_data}/{len(self.insects_data)}\n"
        if patches_with_data > 0:
            summary_text += f"  - Maximum simulation days: {total_days}\n"

        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
                fontfamily='monospace', fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.7))

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _drop_dead_insects(self):
        for df in self.insects_data:
            df.drop(columns=StateNames.DEAD.value, inplace=True)