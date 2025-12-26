import os
import sys
import json
import requests
from datetime import datetime

try:
    from colorama import init as _cinit, Fore, Style
    _cinit(autoreset=True)
except Exception:
    class _F:
        RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"; CYAN="\033[36m"; MAGENTA="\033[35m"
        RESET="\033[0m"; BRIGHT="\033[1m"
    class _S: RESET_ALL="\033[0m"
    Fore=_F(); Style=_S()

# TikTok API endpoint for trending/discover content
# Alternative endpoints to try
TIKTOK_API_ENDPOINTS = [
    "https://www.tiktok.com/api/recommend/item_list/",
    "https://m.tiktok.com/api/recommend/item_list/",
]

def get_mock_trending_videos():
    """
    Generate mock trending videos for demonstration purposes.
    This is used when the API is unavailable.
    
    Returns:
        list: List of mock video data
    """
    mock_videos = [
        {
            "id": "7334567890123456789",
            "title": "Amazing dance challenge! 🔥 #viral #trending #dance",
            "author": "dancer_pro",
            "author_name": "Pro Dancer",
            "thumbnail": "https://via.placeholder.com/300x400/FF0050/FFFFFF?text=TikTok+Video+1",
            "play_url": "",
            "stats": {
                "views": 5420000,
                "likes": 892000,
                "comments": 12500,
                "shares": 45600
            },
            "music": "Original Sound - Pro Dancer",
            "create_time": 1703001234
        },
        {
            "id": "7334567890123456790",
            "title": "Cooking hack that will change your life! 🍳👨‍🍳 #cooking #lifehack #food",
            "author": "chef_master",
            "author_name": "Master Chef",
            "thumbnail": "https://via.placeholder.com/300x400/00D9FF/FFFFFF?text=TikTok+Video+2",
            "play_url": "",
            "stats": {
                "views": 3210000,
                "likes": 654000,
                "comments": 8900,
                "shares": 32100
            },
            "music": "Trendy Beat - DJ Mix",
            "create_time": 1703002345
        },
        {
            "id": "7334567890123456791",
            "title": "Cute pet doing the funniest thing ever 🐶😂 #pets #funny #cute",
            "author": "pet_lover",
            "author_name": "Pet Lover",
            "thumbnail": "https://via.placeholder.com/300x400/FFB800/FFFFFF?text=TikTok+Video+3",
            "play_url": "",
            "stats": {
                "views": 8750000,
                "likes": 1200000,
                "comments": 23400,
                "shares": 67800
            },
            "music": "Happy Song - Music Library",
            "create_time": 1703003456
        },
        {
            "id": "7334567890123456792",
            "title": "Travel vlog: Most beautiful place on Earth! 🌍✨ #travel #nature #explore",
            "author": "travel_guru",
            "author_name": "Travel Guru",
            "thumbnail": "https://via.placeholder.com/300x400/00C851/FFFFFF?text=TikTok+Video+4",
            "play_url": "",
            "stats": {
                "views": 4560000,
                "likes": 723000,
                "comments": 15600,
                "shares": 41200
            },
            "music": "Adventure Theme - Epic Music",
            "create_time": 1703004567
        },
        {
            "id": "7334567890123456793",
            "title": "Mind-blowing magic trick revealed! 🎩✨ #magic #tutorial #amazing",
            "author": "magic_man",
            "author_name": "The Magician",
            "thumbnail": "https://via.placeholder.com/300x400/9933FF/FFFFFF?text=TikTok+Video+5",
            "play_url": "",
            "stats": {
                "views": 6890000,
                "likes": 934000,
                "comments": 18700,
                "shares": 52300
            },
            "music": "Mystery Music - Sound Effects",
            "create_time": 1703005678
        },
        {
            "id": "7334567890123456794",
            "title": "Fashion transformation 2024! 👗💄 #fashion #style #transformation",
            "author": "fashion_queen",
            "author_name": "Fashion Queen",
            "thumbnail": "https://via.placeholder.com/300x400/FF6B9D/FFFFFF?text=TikTok+Video+6",
            "play_url": "",
            "stats": {
                "views": 3450000,
                "likes": 567000,
                "comments": 9800,
                "shares": 28900
            },
            "music": "Pop Hit - Chart Topper",
            "create_time": 1703006789
        },
        {
            "id": "7334567890123456795",
            "title": "Gaming highlights - INSANE clutch! 🎮🔥 #gaming #clutch #highlights",
            "author": "pro_gamer",
            "author_name": "Pro Gamer",
            "thumbnail": "https://via.placeholder.com/300x400/4285F4/FFFFFF?text=TikTok+Video+7",
            "play_url": "",
            "stats": {
                "views": 7230000,
                "likes": 1100000,
                "comments": 21200,
                "shares": 58900
            },
            "music": "Epic Gaming Music - Soundtrack",
            "create_time": 1703007890
        },
        {
            "id": "7334567890123456796",
            "title": "Comedy skit that's too funny! 😂🤣 #comedy #funny #relatable",
            "author": "comedian_pro",
            "author_name": "Comedy Pro",
            "thumbnail": "https://via.placeholder.com/300x400/FFAA00/FFFFFF?text=TikTok+Video+8",
            "play_url": "",
            "stats": {
                "views": 9120000,
                "likes": 1450000,
                "comments": 28900,
                "shares": 72100
            },
            "music": "Comedy Background - Funny Sounds",
            "create_time": 1703008901
        }
    ]
    return mock_videos

def fetch_trending_videos(use_mock=False):
    """
    Fetch trending TikTok videos using TikTok's public API.
    Falls back to mock data if API is unavailable.
    
    Args:
        use_mock (bool): If True, use mock data instead of API
    
    Returns:
        tuple: (success: bool, data: list or error_message: str)
    """
    # If mock mode is enabled, return mock data
    if use_mock:
        return True, get_mock_trending_videos()
    
    # Try multiple API endpoints
    for api_url in TIKTOK_API_ENDPOINTS:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com"
            }
            
            params = {
                "count": 20,
                "itemID": 1,
            }
            
            response = requests.get(api_url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we got valid data
                if "itemList" in data and data["itemList"]:
                    videos = []
                    for item in data["itemList"]:
                        video_info = {
                            "id": item.get("id", ""),
                            "title": item.get("desc", "No description"),
                            "author": item.get("author", {}).get("uniqueId", "Unknown"),
                            "author_name": item.get("author", {}).get("nickname", "Unknown"),
                            "thumbnail": item.get("video", {}).get("cover", ""),
                            "play_url": item.get("video", {}).get("playAddr", ""),
                            "stats": {
                                "views": item.get("stats", {}).get("playCount", 0),
                                "likes": item.get("stats", {}).get("diggCount", 0),
                                "comments": item.get("stats", {}).get("commentCount", 0),
                                "shares": item.get("stats", {}).get("shareCount", 0)
                            },
                            "music": item.get("music", {}).get("title", ""),
                            "create_time": item.get("createTime", 0)
                        }
                        videos.append(video_info)
                    return True, videos
                
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.RequestException:
            continue
        except json.JSONDecodeError:
            continue
        except Exception:
            continue
    
    # If all API endpoints failed, fall back to mock data
    print(f"{Fore.YELLOW}⚠️  API unavailable, using demo data...{Style.RESET_ALL}\n")
    return True, get_mock_trending_videos()

def format_number(num):
    """Format large numbers with K, M suffixes"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def display_trending_videos():
    """Display trending videos in console"""
    print(Fore.MAGENTA + Style.BRIGHT + """
╔════════════════════════════════════════════╗
║                                            ║
║     🔥 TRENDING TIKTOK VIDEOS 🔥          ║
║                                            ║
╚════════════════════════════════════════════╝
""" + Style.RESET_ALL)
    
    print(f"{Fore.YELLOW}⏳ Fetching trending videos...{Style.RESET_ALL}\n")
    
    success, result = fetch_trending_videos()
    
    if not success:
        print(f"{Fore.RED}{Style.BRIGHT}❌ Error: {result}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please check your internet connection and try again.{Style.RESET_ALL}")
        return
    
    videos = result
    print(f"{Fore.GREEN}{Style.BRIGHT}✅ Found {len(videos)} trending videos!{Style.RESET_ALL}\n")
    print("=" * 80)
    
    for idx, video in enumerate(videos, 1):
        print(f"\n{Fore.CYAN}{Style.BRIGHT}#{idx} - {video['title'][:60]}{'...' if len(video['title']) > 60 else ''}{Style.RESET_ALL}")
        print(f"   👤 Author: {video['author_name']} (@{video['author']})")
        print(f"   📊 Stats: 👁️  {format_number(video['stats']['views'])} views | "
              f"❤️  {format_number(video['stats']['likes'])} likes | "
              f"💬 {format_number(video['stats']['comments'])} comments | "
              f"🔄 {format_number(video['stats']['shares'])} shares")
        if video['music']:
            print(f"   🎵 Music: {video['music']}")
        print(f"   🔗 https://www.tiktok.com/@{video['author']}/video/{video['id']}")
        print("-" * 80)
    
    print(f"\n{Fore.GREEN}💡 Tip: Visit the links above to watch the videos!{Style.RESET_ALL}\n")

def generate_html_page(output_file="trending_videos.html"):
    """Generate an HTML page with trending videos"""
    print(f"{Fore.YELLOW}⏳ Generating HTML page...{Style.RESET_ALL}\n")
    
    success, result = fetch_trending_videos()
    
    if not success:
        print(f"{Fore.RED}{Style.BRIGHT}❌ Error: {result}{Style.RESET_ALL}")
        return False
    
    videos = result
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Trending TikTok Videos</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .video-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .video-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }
        
        .video-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .video-thumbnail {
            width: 100%;
            height: 400px;
            object-fit: cover;
            background: #f0f0f0;
        }
        
        .video-info {
            padding: 20px;
        }
        
        .video-title {
            font-size: 1em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .video-author {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
        }
        
        .video-stats {
            display: flex;
            justify-content: space-between;
            font-size: 0.85em;
            color: #888;
            margin-bottom: 10px;
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .music-info {
            font-size: 0.85em;
            color: #888;
            font-style: italic;
            margin-top: 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .view-button {
            display: block;
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 15px;
            transition: opacity 0.3s ease;
        }
        
        .view-button:hover {
            opacity: 0.9;
        }
        
        footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9em;
        }
        
        .error-message {
            background: #ff6b6b;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }
        
        @media (max-width: 768px) {
            header h1 {
                font-size: 2em;
            }
            
            .video-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 Trending TikTok Videos</h1>
            <p>Discover what's viral right now!</p>
        </header>
        
        <div class="video-grid">
"""
    
    for video in videos:
        video_url = f"https://www.tiktok.com/@{video['author']}/video/{video['id']}"
        html_content += f"""
            <div class="video-card" onclick="window.open('{video_url}', '_blank')">
                <img class="video-thumbnail" src="{video['thumbnail']}" alt="{video['title']}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22300%22 height=%22400%22%3E%3Crect fill=%22%23ddd%22 width=%22300%22 height=%22400%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 fill=%22%23999%22%3ENo Image%3C/text%3E%3C/svg%3E'">
                <div class="video-info">
                    <div class="video-title">{video['title']}</div>
                    <div class="video-author">👤 {video['author_name']} (@{video['author']})</div>
                    <div class="video-stats">
                        <div class="stat-item">👁️ {format_number(video['stats']['views'])}</div>
                        <div class="stat-item">❤️ {format_number(video['stats']['likes'])}</div>
                        <div class="stat-item">💬 {format_number(video['stats']['comments'])}</div>
                        <div class="stat-item">🔄 {format_number(video['stats']['shares'])}</div>
                    </div>
"""
        if video['music']:
            html_content += f"""                    <div class="music-info">🎵 {video['music']}</div>
"""
        html_content += f"""                    <a href="{video_url}" class="view-button" target="_blank" onclick="event.stopPropagation()">Watch on TikTok</a>
                </div>
            </div>
"""
    
    html_content += """        </div>
        
        <footer>
            <p>Generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p>Data fetched from TikTok's public API</p>
        </footer>
    </div>
</body>
</html>
"""
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ HTML page generated successfully: {output_file}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Open '{output_file}' in your browser to view the trending videos!{Style.RESET_ALL}\n")
        return True
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}❌ Error writing HTML file: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    """Main function to run the trending videos feature"""
    os.system("cls" if os.name == "nt" else "clear")
    
    print(Fore.MAGENTA + Style.BRIGHT + """
╔════════════════════════════════════════════╗
║                                            ║
║     🔥 TRENDING TIKTOK VIEWER 🔥          ║
║                                            ║
╠════════════════════════════════════════════╣
║  1. 📺 Display trending videos in console  ║
║  2. 🌐 Generate HTML page                  ║
║  3. 🔄 Both (Console + HTML)               ║
╚════════════════════════════════════════════╝
""" + Style.RESET_ALL)
    
    choice = input(Fore.YELLOW + "👉 Choose option (1-3): " + Style.RESET_ALL).strip()
    
    if choice == "1":
        display_trending_videos()
    elif choice == "2":
        generate_html_page()
    elif choice == "3":
        display_trending_videos()
        print("\n" + "=" * 80 + "\n")
        generate_html_page()
    else:
        print(Fore.RED + "❌ Invalid choice!" + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}⏹ Stopped by user.{Style.RESET_ALL}")
