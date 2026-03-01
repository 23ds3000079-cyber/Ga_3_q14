#!/usr/bin/env python3
"""
Scrape seeds 41-50 using Playwright (sync version)
"""

import sys
from playwright.sync_api import sync_playwright

def scrape_all_seeds():
    """Scrape all seeds 41-50"""
    
    seeds = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    all_numbers = []
    seed_sums = {}
    
    print("="*60)
    print("Q14 - Seeds 41-50 Scraper")
    print("="*60)
    print("23ds3000079@ds.study.iitm.ac.in")
    print("="*60)
    
    with sync_playwright() as p:
        # Launch browser with proper args for GitHub Actions
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        for seed in seeds:
            print(f"\n📊 Processing seed {seed}...")
            page = None
            
            try:
                page = browser.new_page()
                url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
                
                # Navigate and wait for JavaScript
                page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait for table and ensure it's loaded
                page.wait_for_selector("table", timeout=5000)
                page.wait_for_timeout(2000)
                
                # Extract numbers from table
                numbers = page.evaluate('''
                    () => {
                        const nums = [];
                        const rows = document.querySelectorAll('table tr');
                        for (const row of rows) {
                            const cells = row.querySelectorAll('td');
                            for (const cell of cells) {
                                const text = cell.textContent.trim();
                                if (text && /^\\d+$/.test(text)) {
                                    nums.push(parseInt(text, 10));
                                }
                            }
                        }
                        return nums;
                    }
                ''')
                
                if numbers:
                    seed_sum = sum(numbers)
                    seed_sums[seed] = seed_sum
                    all_numbers.extend(numbers)
                    
                    print(f"   ✅ Found {len(numbers)} numbers")
                    print(f"   ✅ Sample: {numbers[:5]}")
                    print(f"   ✅ Sum: {seed_sum}")
                else:
                    print(f"   ❌ No numbers found")
                    
            except Exception as e:
                print(f"   ❌ Error: {type(e).__name__}: {e}")
            finally:
                if page:
                    page.close()
        
        browser.close()
    
    # Calculate and display results
    grand_total = sum(seed_sums.values())
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    for seed in seeds:
        if seed in seed_sums:
            print(f"Seed {seed:2d}: {seed_sums[seed]:8,}")
    
    print("-"*60)
    print(f"GRAND TOTAL: {grand_total:10,}")
    print("="*60)
    print(f"Total numbers collected: {len(all_numbers)}")
    print("="*60)
    
    # Save results
    with open('results.txt', 'w') as f:
        f.write(f"Grand Total: {grand_total}\n")
        f.write(f"Total Numbers: {len(all_numbers)}\n")
        for seed in seeds:
            if seed in seed_sums:
                f.write(f"Seed {seed}: {seed_sums[seed]}\n")
    
    return grand_total

if __name__ == "__main__":
    try:
        total = scrape_all_seeds()
        print(f"\n✅ Script completed successfully")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Script failed: {e}", file=sys.stderr)
        sys.exit(1)
