#!/usr/bin/env python3
"""
Scrape seeds 41-50 and calculate total sum - FIXED VERSION
"""

import requests
import re
import sys

def scrape_seed(seed):
    """Scrape a single seed page and return ALL numbers from the table"""
    url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        # Method 1: Find table structure
        html = response.text
        
        # Look for the table content
        table_match = re.search(r'<table>(.*?)</table>', html, re.DOTALL)
        if not table_match:
            return []
        
        table_content = table_match.group(1)
        
        # Find all numbers in table cells (td tags)
        # This regex looks for numbers inside <td> or <th> tags
        numbers = re.findall(r'<t[dh][^>]*>(\d+)</t[dh]>', table_content, re.IGNORECASE)
        
        # Convert to integers
        numbers = [int(n) for n in numbers]
        
        return numbers
        
    except Exception as e:
        print(f"Error scraping seed {seed}: {e}", file=sys.stderr)
        return []

def main():
    """Main function to scrape all seeds 41-50"""
    
    seeds = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    all_numbers = []
    seed_sums = {}
    
    print("="*60)
    print("Q14 - DataDash Seeds 41-50 Scraper (FIXED)")
    print("="*60)
    print("23ds3000079@ds.study.iitm.ac.in")
    print("="*60)
    
    for seed in seeds:
        print(f"\n📊 Processing seed {seed}...")
        
        numbers = scrape_seed(seed)
        
        if numbers:
            seed_sum = sum(numbers)
            seed_sums[seed] = seed_sum
            all_numbers.extend(numbers)
            
            print(f"   ✅ Found {len(numbers)} numbers")
            print(f"   ✅ First 10: {numbers[:10]}")
            print(f"   ✅ Last 10: {numbers[-10:]}")
            print(f"   ✅ Sum: {seed_sum}")
        else:
            print(f"   ❌ No numbers found for seed {seed}")
            # Debug: print part of the HTML
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}", timeout=5, headers=headers)
                print(f"   HTML preview: {r.text[:500]}")
            except:
                pass
    
    # Calculate grand total
    grand_total = sum(seed_sums.values())
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    # Print individual seed sums
    for seed in seeds:
        if seed in seed_sums:
            print(f"Seed {seed:2d}: {seed_sums[seed]:8,}")
        else:
            print(f"Seed {seed:2d}: FAILED")
    
    print("-"*60)
    print(f"GRAND TOTAL: {grand_total:10,}")
    print("="*60)
    print(f"Total numbers collected: {len(all_numbers)}")
    print("="*60)
    
    # Expected: 500 numbers per seed (5 rows × 4 columns = 20 numbers? Wait, that's too small)
    # Actually each seed should have 5 rows × 4 columns = 20 numbers? No, that's what you got (2 per seed)
    # Let's calculate properly - if each cell has numbers, and there are 5x4=20 cells, that's 20 numbers per seed
    # But you got 2 numbers per seed (row and col indices), so you need the actual data values
    
    expected = 20 * len(seeds)  # 20 cells per table × 10 seeds = 200 numbers
    print(f"Expected numbers (if 5x4 table): {expected}")
    print(f"Actual numbers found: {len(all_numbers)}")
    
    # Save to file
    with open('results.txt', 'w') as f:
        f.write(f"Grand Total: {grand_total}\n")
        f.write(f"Total Numbers: {len(all_numbers)}\n")
        f.write(f"Seeds: {seeds}\n")
        f.write(f"Individual Sums: {seed_sums}\n")
        f.write(f"All Numbers: {sorted(all_numbers)}\n")
    
    return grand_total

if __name__ == "__main__":
    try:
        total = main()
        print(f"\n✅ Script completed successfully")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Script failed: {e}", file=sys.stderr)
        sys.exit(1)
