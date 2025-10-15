import subprocess
import pandas as pd
import numpy as np
from pathlib import Path
import json
import sys

def run_single_simulation(run_number):
    """Run a single simulation and return the results"""
    print(f"\n{'='*80}")
    print(f"RUNNING SIMULATION {run_number}/10 (Seed: {100 + run_number})")
    print(f"{'='*80}\n")
    
    # Run the simulation with a different seed
    # Pass the seed as an environment variable or command line argument
    import os
    env = os.environ.copy()
    env['RANDOM_SEED'] = str(100 + run_number)
    
    result = subprocess.run(
        [sys.executable, 'run_simulation.py', '--seed', str(100 + run_number)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
        env=env
    )
    
    # Read the results CSV file
    results_path = Path(__file__).parent.parent / 'day1_placement_results.csv'
    df = pd.read_csv(results_path)
    
    # Calculate statistics
    placed = df[df['status'] == 'Placed']
    opted_out = df[df['status'] == 'Opted_Out']
    unplaced = df[df['status'] == 'Unplaced']
    
    stats = {
        'run_number': run_number,
        'total_students': len(df),
        'total_placed': len(placed),
        'total_opted_out': len(opted_out),
        'total_unplaced': len(unplaced),
        'placement_rate': (len(placed) / len(df)) * 100,
        'opt_out_rate': (len(opted_out) / len(df)) * 100,
        'companies_hired': placed['placed_company'].nunique() if len(placed) > 0 else 0,
    }
    
    # Get company-wise counts
    if len(placed) > 0:
        company_counts = placed['placed_company'].value_counts().to_dict()
        stats['company_counts'] = company_counts
    else:
        stats['company_counts'] = {}
    
    # Get department-wise counts
    if len(placed) > 0:
        dept_counts = placed['department'].value_counts().to_dict()
        stats['dept_counts'] = dept_counts
    else:
        stats['dept_counts'] = {}
    
    print(f"Run {run_number} Results:")
    print(f"  Placed: {stats['total_placed']}")
    print(f"  Opted Out: {stats['total_opted_out']}")
    print(f"  Placement Rate: {stats['placement_rate']:.2f}%")
    
    return stats

def main():
    print("\n" + "="*80)
    print("RUNNING 10 SIMULATIONS")
    print("="*80)
    
    all_runs = []
    
    # Run 10 simulations
    for i in range(1, 11):
        stats = run_single_simulation(i)
        all_runs.append(stats)
    
    # Calculate averages
    print("\n\n" + "="*80)
    print("CALCULATING AVERAGE STATISTICS")
    print("="*80 + "\n")
    
    avg_placed = np.mean([r['total_placed'] for r in all_runs])
    std_placed = np.std([r['total_placed'] for r in all_runs])
    min_placed = min([r['total_placed'] for r in all_runs])
    max_placed = max([r['total_placed'] for r in all_runs])
    
    avg_opted_out = np.mean([r['total_opted_out'] for r in all_runs])
    std_opted_out = np.std([r['total_opted_out'] for r in all_runs])
    
    avg_placement_rate = np.mean([r['placement_rate'] for r in all_runs])
    std_placement_rate = np.std([r['placement_rate'] for r in all_runs])
    
    avg_opt_out_rate = np.mean([r['opt_out_rate'] for r in all_runs])
    
    avg_companies_hired = np.mean([r['companies_hired'] for r in all_runs])
    
    # Company-wise averages
    all_companies = set()
    for run in all_runs:
        all_companies.update(run['company_counts'].keys())
    
    company_avg = {}
    company_std = {}
    for company in all_companies:
        counts = [run['company_counts'].get(company, 0) for run in all_runs]
        company_avg[company] = np.mean(counts)
        company_std[company] = np.std(counts)
    
    # Department-wise averages
    all_depts = set()
    for run in all_runs:
        all_depts.update(run['dept_counts'].keys())
    
    dept_avg = {}
    dept_std = {}
    for dept in all_depts:
        counts = [run['dept_counts'].get(dept, 0) for run in all_runs]
        dept_avg[dept] = np.mean(counts)
        dept_std[dept] = np.std(counts)
    
    # Print results
    print("="*80)
    print("OVERALL STATISTICS (10 RUNS)")
    print("="*80)
    print(f"\nTotal Students per Run: {all_runs[0]['total_students']}")
    print(f"\nPlacements:")
    print(f"  Average: {avg_placed:.1f} ± {std_placed:.1f}")
    print(f"  Min: {min_placed}")
    print(f"  Max: {max_placed}")
    print(f"  Placement Rate: {avg_placement_rate:.2f}% ± {std_placement_rate:.2f}%")
    
    print(f"\nOpt-Outs:")
    print(f"  Average: {avg_opted_out:.1f} ± {std_opted_out:.1f}")
    print(f"  Opt-Out Rate: {avg_opt_out_rate:.2f}%")
    
    print(f"\nCompanies Hired: {avg_companies_hired:.1f}")
    
    print("\n" + "="*80)
    print("COMPANY-WISE AVERAGES (Sorted by Average Hires)")
    print("="*80 + "\n")
    
    sorted_companies = sorted(company_avg.items(), key=lambda x: x[1], reverse=True)
    for company, avg_count in sorted_companies:
        std_count = company_std[company]
        print(f"{company:<45} : {avg_count:>5.1f} ± {std_count:>4.1f} students")
    
    print("\n" + "="*80)
    print("DEPARTMENT-WISE AVERAGES (Sorted by Average Placements)")
    print("="*80 + "\n")
    
    sorted_depts = sorted(dept_avg.items(), key=lambda x: x[1], reverse=True)
    for dept, avg_count in sorted_depts:
        std_count = dept_std[dept]
        # Get total students in department from first run
        total_in_dept = len([s for s in pd.read_csv(Path(__file__).parent.parent / 'day1_placement_results.csv').itertuples() if s.department == dept])
        if total_in_dept > 0:
            placement_rate = (avg_count / total_in_dept) * 100
            print(f"{dept:<10} : {avg_count:>5.1f} ± {std_count:>4.1f} ({placement_rate:>5.2f}% avg placement rate)")
    
    # Print individual run details
    print("\n" + "="*80)
    print("INDIVIDUAL RUN DETAILS")
    print("="*80 + "\n")
    
    print(f"{'Run':<6} {'Placed':<10} {'Opted Out':<12} {'Placement %':<15} {'Companies':<12}")
    print("-" * 80)
    for run in all_runs:
        print(f"{run['run_number']:<6} {run['total_placed']:<10} {run['total_opted_out']:<12} "
              f"{run['placement_rate']:<14.2f}% {run['companies_hired']:<12}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    
    # Save detailed results to JSON
    output_file = Path(__file__).parent / 'multiple_runs_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'all_runs': all_runs,
            'summary': {
                'avg_placed': avg_placed,
                'std_placed': std_placed,
                'min_placed': min_placed,
                'max_placed': max_placed,
                'avg_opted_out': avg_opted_out,
                'std_opted_out': std_opted_out,
                'avg_placement_rate': avg_placement_rate,
                'std_placement_rate': std_placement_rate,
                'avg_opt_out_rate': avg_opt_out_rate,
                'avg_companies_hired': avg_companies_hired,
            },
            'company_averages': company_avg,
            'company_std': company_std,
            'dept_averages': dept_avg,
            'dept_std': dept_std,
        }, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: {output_file}")

if __name__ == '__main__':
    main()
