#!/usr/bin/env python3
"""
Scrape seeds 41-50 - USING PLAYWRIGHT FOR DYNAMIC CONTENT
"""

import sys
import asyncio
from playwright.async_api import async_playwright

async def scrape_seed(seed):
    """Scrape a single seed page using Playwright to handle JavaScript"""
    url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        try:
            page = await browser.new_page()
            
            # Navigate and wait for JavaScript to execute
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for table to be present
            await page.wait_for_selector("table", timeout=5000)
            
            # Additional wait for any dynamic content
            await page.wait_for_timeout(2000)
            
            # Extract ALL numbers from the table
            numbers = await page.evaluate('''
                () => {
                    const nums = [];
                    // Get all cells in the table
                    const cells = document.querySelectorAll('table td, table th');
                    cells.forEach(cell => {
                        const text = cell.textContent.trim();
                        // Only get numbers (ignore empty cells)
                        if (text && !isNaN(parseInt(text)) && text !== '') {
                            nums.push(parseInt(text, 10));
                        }
                    });
                    return nums;
                }
            ''')
            
            await browser.close()
            return numbers
            
        except Exception as e:
            print(f"Error scraping seed {seed}: {e}", file=sys.stderr)
            await browser.close()
            return []

async def main():
    """Main function to scrape all seeds 41-50"""
    
    seeds = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    all_numbers = []
    seed_sums = {}
    
    print("="*60)
    print("Q14 - Seeds 41-50 Scraper (Playwright)")
    print("="*60)
    print("23ds3000079@ds.study.iitm.ac.in")
    print("="*60)
    
    for seed in seeds:
        print(f"\n📊 Processing seed {seed}...")
        
        numbers = await scrape_seed(seed)
        
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
    
    # Calculate grand total
    grand_total = sum(seed_sums.values())
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
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
    
    # Save results
    with open('results.txt', 'w') as f:
        f.write(f"Grand Total: {grand_total}\n")
        f.write(f"Total Numbers: {len(all_numbers)}\n")
        f.write(f"Individual Sums: {seed_sums}\n")
    
    return grand_total

if __name__ == "__main__":
    try:
        total = asyncio.run(main())
        print(f"\n✅ Script completed successfully with total: {total}")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Script failed: {e}", file=sys.stderr)
        sys.exit(1)
