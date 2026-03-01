import requests
import re

# Seeds 41-50
seeds = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
grand_total = 0

print("="*60)
print("Q14 - Seeds 41-50 Scraper")
print("="*60)

for seed in seeds:
    url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
    print(f"\nFetching seed {seed}...")
    
    try:
        # Simple request without any fancy parsing
        response = requests.get(url, timeout=10)
        
        # Find all numbers using regex
        numbers = re.findall(r'>(\d+)<', response.text)
        numbers = [int(n) for n in numbers]
        
        if numbers:
            seed_sum = sum(numbers)
            print(f"  Found {len(numbers)} numbers")
            print(f"  Sum: {seed_sum}")
            grand_total += seed_sum
        else:
            print(f"  No numbers found")
            
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "="*60)
print(f"GRAND TOTAL: {grand_total}")
print("="*60)
