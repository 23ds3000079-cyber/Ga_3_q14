#!/usr/bin/env python3
"""
Scrape seeds 41-50 and calculate total sum
"""

import requests
import re
import sys

def scrape_seed(seed):
    """Scrape a single seed page and return the sum of numbers"""
    url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
    
    try:
        # Make request with headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        # Method 1: Find all numbers in the HTML
        # Look for patterns like >123< which indicates numbers in HTML tags
        numbers = re.findall(r'>(\d+)<', response.text)
        
        # Method 2: Also find standalone numbers
        numbers += re.findall(r'\b(\d+)\b', response.text)
        
        # Convert to integers and remove duplicates
        numbers = [int(n) for n in numbers if n.isdigit()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_numbers = []
        for n in numbers:
            if n not in seen and n > 0:
                seen.add(n)
                unique_numbers.append(n)
        
        return unique_numbers
        
    except Exception as e:
        print(f"Error scraping seed {seed}: {e}", file=sys.stderr)
        return []

def main():
    """Main function to scrape all seeds 41-50"""
    
    seeds = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    all_numbers = []
    seed_sums = {}
    
    print("="*60)
    print("Q14 - DataDash Seeds 41-50 Scraper")
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
            print(f"   ✅ First 5: {numbers[:5]}")
            print(f"   ✅ Last 5: {numbers[-5:]}")
            print(f"   ✅ Sum: {seed_sum}")
        else:
            print(f"   ❌ No numbers found for seed {seed}")
    
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
    
    # Verify we got expected count (500 per seed)
    expected = 500 * len(seeds)
    if len(all_numbers) == expected:
        print(f"✅ Correct! Found all {expected} numbers")
    else:
        print(f"⚠️ Expected {expected} numbers, found {len(all_numbers)}")
    
    # Save to file for artifact
    with open('results.txt', 'w') as f:
        f.write(f"Grand Total: {grand_total}\n")
        f.write(f"Total Numbers: {len(all_numbers)}\n")
        f.write(f"Seeds: {seeds}\n")
        f.write(f"Individual Sums: {seed_sums}\n")
    
    return grand_total

if __name__ == "__main__":
    try:
        total = main()
        print(f"\n✅ Script completed successfully with total: {total}")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Script failed: {e}", file=sys.stderr)
        sys.exit(1)
