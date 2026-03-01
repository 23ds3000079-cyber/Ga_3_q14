from playwright.sync_api import sync_playwright
import time

def scrape_seeds_41_to_50():
    seeds = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    grand_total = 0
    all_numbers = []
    
    print("="*60)
    print("DataDash QA Automation - Seeds 41-50")
    print("="*60)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        for seed in seeds:
            page = None
            try:
                print(f"\n📌 Processing seed {seed}...")
                page = browser.new_page()
                
                url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
                print(f"   URL: {url}")
                
                # Navigate and wait for JavaScript to execute
                page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait for table to load
                page.wait_for_selector("table", timeout=5000)
                page.wait_for_timeout(2000)  # Extra safety
                
                # Extract numbers from the table
                numbers = page.evaluate('''
                    () => {
                        const nums = [];
                        // Select all table cells
                        const cells = document.querySelectorAll('table td, table th');
                        cells.forEach(cell => {
                            const text = cell.textContent.trim();
                            // Check if it's a number
                            if (text && /^\d+$/.test(text)) {
                                nums.push(parseInt(text, 10));
                            }
                        });
                        return nums;
                    }
                ''')
                
                if numbers and len(numbers) > 0:
                    seed_sum = sum(numbers)
                    print(f"   ✅ Found {len(numbers)} numbers")
                    print(f"   ✅ First 10: {numbers[:10]}")
                    print(f"   ✅ Last 10: {numbers[-10:]}")
                    print(f"   ✅ Sum for seed {seed}: {seed_sum}")
                    
                    grand_total += seed_sum
                    all_numbers.extend(numbers)
                else:
                    print(f"   ⚠️ No numbers found!")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            finally:
                if page:
                    page.close()
        
        browser.close()
    
    # Final output
    print("\n" + "="*60)
    print("📊 FINAL RESULTS - SEEDS 41-50")
    print("="*60)
    print(f"Total numbers found across all seeds: {len(all_numbers)}")
    print(f"GRAND TOTAL SUM: {grand_total}")
    print("="*60)
    
    # Verify we got all 5000 numbers (500 per page × 10 pages)
    expected_total = 500 * len(seeds)
    if len(all_numbers) == expected_total:
        print(f"✅ Correct! Found all {expected_total} numbers")
    else:
        print(f"⚠️ Expected {expected_total} numbers, found {len(all_numbers)}")
    
    return grand_total

if __name__ == "__main__":
    total = scrape_seeds_41_to_50()
