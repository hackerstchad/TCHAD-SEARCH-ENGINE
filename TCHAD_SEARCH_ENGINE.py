#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCHAD SEARCH ENGINE v10.0 - Moteur de Recherche Avancé
Développé par HiddenWorld Communauté Tchadienne
Inspiré de Yandex, Google, Bing avec fonctionnalités modernes.

Usage strictement légal et éducatif.
"""

import os
import re
import sys
import json
import time
import math
import queue
import random
import hashlib
import argparse
import threading
import urllib.parse
import urllib.request
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION GLOBALE
# ═══════════════════════════════════════════════════════════════════
VERSION = "10.0"
APP_NAME = "TCHAD SEARCH ENGINE"
DEVELOPER = "HiddenWorld Communauté Tchadienne"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

SEARCH_ENGINES = {
    "google": {
        "url": "https://www.google.com/search",
        "param": "q",
        "start": "start",
        "step": 10,
    },
    "bing": {
        "url": "https://www.bing.com/search",
        "param": "q",
        "start": "first",
        "step": 10,
    },
    "duckduckgo": {
        "url": "https://html.duckduckgo.com/html/",
        "param": "q",
        "start": "s",
        "step": 30,
    },
    "yandex": {
        "url": "https://yandex.com/search/",
        "param": "text",
        "start": "p",
        "step": 1,
    },
    "yahoo": {
        "url": "https://search.yahoo.com/search",
        "param": "p",
        "start": "b",
        "step": 10,
    },
    "brave": {
        "url": "https://search.brave.com/search",
        "param": "q",
        "start": "offset",
        "step": 10,
    },
    "ecosia": {
        "url": "https://www.ecosia.org/search",
        "param": "q",
        "start": "p",
        "step": 10,
    },
}

LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "ar": "العربية",
    "zh": "中文",
    "ru": "Русский",
    "pt": "Português",
    "ja": "日本語",
    "ko": "한국어",
    "it": "Italiano",
    "nl": "Nederlands",
    "tr": "Türkçe",
    "pl": "Polski",
    "sv": "Svenska",
}

COUNTRIES = {
    "fr": "France",
    "us": "États-Unis",
    "uk": "Royaume-Uni",
    "ca": "Canada",
    "de": "Allemagne",
    "es": "Espagne",
    "it": "Italie",
    "jp": "Japon",
    "cn": "Chine",
    "ru": "Russie",
    "br": "Brésil",
    "in": "Inde",
    "au": "Australie",
    "td": "Tchad",
    "ng": "Nigeria",
    "za": "Afrique du Sud",
}

# ═══════════════════════════════════════════════════════════════════
# COULEURS ET STYLES
# ═══════════════════════════════════════════════════════════════════
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BLACK = Fore.BLACK
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
                                                                    ..::::::::::::::::::::::::::::::
                          .-+**###%%%%%%##*+=:.                      .::::::::::::::::::::::::::::::
                     -+****######%%%%%%%%%%%%#####**-                  .::::::::::::::::::::::::::::
                  :=++****#####%%%%%%%%%%%%%%%%#####****=.              .:::::::::::::::::::::::::::
                .-=+++****#####%%%%%%%%%%%%%%%%######****++:             .::::::::::::::::::::::::::
                -==++++***######%%%%%%%%%%%%%%%%#####****++=-             ::::::::::::::::::::::::::
               :-====+++**#######%%%%%%%%%%%%%%%######***++=-:            .:::::::::::::::::::::::::
              .------========+####%%%@@%%%%%%%#########**+=+=-             :::::::::::::::::::::::::
              :-:-:         -+=+*#%%%%%@%%%%%%%#*++=========--.            .::::::::::::::::::::::::
             .-:.:=====+++=:   -*+*%%%@@%%%##+=++=-.     .:::-:            .::::::::::::::::::::::::
             :-.-+++++++++++=+: .+**%@%%%#*+++:     .-====:. .:            .::::::::::::::::::::::--
             :::=+***###***+++=---#%%%@%#**+. .:-=++******+=-.:             ::::::::::::::::::::::--
             ::-=+*#########**++===*%@%%%#*+=-=+**#######***=:.             :::::::::::::::::-------
             ::-=+*+=-=+**+++*#**++=#%%%%#==+**##########***+:.             :::::::::::::::---------
             -=-=++-=       .=*+=+++#%%%%*+**+++******=-+**++:.            .::::::::::::::----------
            .=====-#=.         .==**#%%%#++++:         ==-*+=.:            .:::::::-----------------
.          .-==+****+++******++*****%%%%#+*#++#*=:.    .----:+.            :::::::::----------------
.           -=***#####%%%%%%%%%##***%%%%#**##%%%#**+++++***+==.            :::::--------------------
.           :+***####%%%%%%%%%%#***#%%%%#**##%%%%%%%%######**-.           .:::::--------------------
..          :+*****###%%%%%%%%##***#%@%%#***#%%%%%%%#######**+.           ..::::--------------------
..          .=+****####%%%%%%##***#%%%%%#***#%%%%%%#######***+:       .    ..:::--------------------
..          .:=+****#####*++=*##**#%@@%%#**###%%%%%###******+=.   -+**:     .::::-------------------
..           =::=+++====+***+*##**#%@@%%#+*##**+=+**#*****+=:-  :#%%%##*.   ..:::-------------------
.           .:==.::=**######++: -+=+#**++=-:==##**+===+==-.:*.  -##%%%#**. . .:::-------------------
.           . ==-:  .*######%%%%+   ...  =*##%%####***. .=-=.    +##%%###*. ..:::-------------------
.            .:==:+   -####%#%%.   .  .   +%%######**  :-=+     .-##%%%%#*+ ...::-------------------
.            . :+=:*.             :%%@-     =**##*=.  *:=+      ..+#%%%%%##-...::-------------------
.            ...-++:+*=---:::....*%%%%%#:         . .*:+= .   ..  :#%%%%%%%*:..::-------------------
.             ..:-++-.+#######%%####***+++++#######*--+=.   ...    =#%%%%%%#*..:--------------------
.              ..:-++--=-=*##%%%%%%%%%%%%#######*=:-++-..  ..      .#%%%@%%%#+:::-------------------
.               :::-++==+***++==-----=++*+++====+==*+:.......       =#%%@%%%%#+---------------------
.                :--:+*+=+*######:    :********+=+#+.:.....         .#%@%%%%###=--------------------
.                 .--:+*++*###%%%-.-:.#%%%%##*++**=..:...            +%%%%%%###*--------------------
..                  -=-=****##%%* :=: *%%%##*+**+:::....             :#%%#%%####*+*##*+=------------
..                   .--=***##%%+ ... *%%##****=.:. .                 +#%%%%%%%%###%%%%%#*=-=---==--
...                    .-=**##%%+    .#%##***=::...                   :*#%%%%%%%%##%%%%%%##*=-======
...                      .-+*####    +%##**+-:..                       -*#%%%%@%%%#*%%%%%%%##*======
                           .=+**#-  .###*+=.. .                        .=*#%%@@@%%%##%%%@%%%%##+-===
                              :=+-  -*+=:. .                     -+*+-  .=*#%%%%%%%%##%%%%%%%%##+===
                                                               *#######*. -*%%%%%%%%%##%%%%%%%###*==
                                                              -##%##%%#%#+ -#%%%%%%%%%###%%%%%%%##**
                                                              :##%%%%%%%%%#:*#%%%%%%%%####%%%%%%###*
                                                              .*#%%%%%%%%%%#*#%%%%%%%######%%%%%%%#*
                                                          . .. -#%%%%%%%%%%###%%%%%%%%%#####%%%%%%%%
                                                         :#*####**##%%%%%%%%#%#%%%%%%%%%######%%%%%%
                                                        .**###%%%#**#%%%%%%%%%%%%%%%%%%%%##*##%%%%%#
                                                        -***##%%%%#*#%%%%%%%%%%%%%%%%%%%###***#####*
                                                        :**##########%%%%%%%%%%%%%%%%%%####***####**
                                                         +***######%%%%%%%%%%%%%%%%#####************
                                                         :+***####%%%%%%%%%%####%#%###******++******


████████╗ ██████╗██╗  ██╗ █████╗ ██████╗       ███████╗███████╗██████╗  ██████╗██╗  ██╗      ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗
╚══██╔══╝██╔════╝██║  ██║██╔══██╗██╔══██╗      ██╔════╝██╔════╝██╔══██╗██╔════╝██║  ██║      ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝
   ██║   ██║     ███████║███████║██║  ██║█████╗███████╗█████╗  ██████╔╝██║     ███████║█████╗█████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  
   ██║   ██║     ██╔══██║██╔══██║██║  ██║╚════╝╚════██║██╔══╝  ██╔══██╗██║     ██╔══██║╚════╝██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  
   ██║   ╚██████╗██║  ██║██║  ██║██████╔╝      ███████║███████╗██║  ██║╚██████╗██║  ██║      ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗
   ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝       ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝      ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝
                                                                                                                                             
{Colors.RESET}
{Colors.GREEN}{Colors.BOLD}        {APP_NAME} v{VERSION} - Moteur de Recherche Mondial{Colors.RESET}
{Colors.YELLOW}        Développé par {DEVELOPER}{Colors.RESET}
    """)

def log(msg, level="INFO"):
    colors = {
        "INFO": Colors.CYAN,
        "OK": Colors.GREEN,
        "WARN": Colors.YELLOW,
        "ERROR": Colors.RED,
        "SEARCH": Colors.BLUE,
        "RESULT": Colors.MAGENTA,
    }
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {colors.get(level, Colors.WHITE)}[{level}]{Colors.RESET} {msg}")

# ═══════════════════════════════════════════════════════════════════
# INDEX LOCAL SIMPLE
# ═══════════════════════════════════════════════════════════════════
class LocalIndex:
    def __init__(self, index_dir=".tchad_index"):
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.documents_file = os.path.join(index_dir, "documents.json")
        self.index_file = os.path.join(index_dir, "inverted_index.json")
        self.documents = self.load_json(self.documents_file, {})
        self.inverted_index = self.load_json(self.index_file, defaultdict(list))

    def load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return default

    def save(self):
        with open(self.documents_file, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(dict(self.inverted_index), f, ensure_ascii=False, indent=2)

    def tokenize(self, text):
        return re.findall(r'\b[a-zA-ZÀ-ÿ0-9_]{2,}\b', text.lower())

    def add_document(self, url, title, snippet):
        doc_id = hashlib.md5(url.encode()).hexdigest()
        self.documents[doc_id] = {
            "url": url,
            "title": title,
            "snippet": snippet,
            "timestamp": datetime.now().isoformat(),
        }
        text = f"{title} {snippet}"
        tokens = self.tokenize(text)
        for token in tokens:
            if doc_id not in self.inverted_index[token]:
                self.inverted_index[token].append(doc_id)
        self.save()
        return doc_id

    def search(self, query, top_n=20):
        tokens = self.tokenize(query)
        if not tokens:
            return []
        scores = Counter()
        for token in tokens:
            for doc_id in self.inverted_index.get(token, []):
                scores[doc_id] += 1
        results = []
        for doc_id, score in scores.most_common(top_n):
            doc = self.documents.get(doc_id, {})
            doc["score"] = score
            results.append(doc)
        return results

# ═══════════════════════════════════════════════════════════════════
# MOTEUR DE RECHERCHE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
class TchadSearchEngine:
    def __init__(self, engine="duckduckgo", lang="fr", country="fr", safe_search="moderate"):
        self.engine = engine
        self.lang = lang
        self.country = country
        self.safe_search = safe_search
        self.timeout = 15
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": f"{lang}-{country.upper()},{lang};q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
        })
        self.index = LocalIndex()
        self.history = []
        self.results_cache = {}

    def get_random_agent(self):
        return random.choice(USER_AGENTS)

    def set_engine(self, engine):
        if engine in SEARCH_ENGINES:
            self.engine = engine
            return True
        return False

    def search(self, query, pages=1, save_to_index=True):
        if not query:
            log("Requête vide", "ERROR")
            return []

        log(f"Recherche: '{query}' via {self.engine.upper()}", "SEARCH")
        cache_key = f"{self.engine}:{self.lang}:{self.country}:{query}:{pages}"
        if cache_key in self.results_cache:
            log("Résultats trouvés en cache", "OK")
            return self.results_cache[cache_key]

        all_results = []
        engine_config = SEARCH_ENGINES.get(self.engine, SEARCH_ENGINES["duckduckgo"])

        with ThreadPoolExecutor(max_workers=min(pages, 5)) as executor:
            futures = []
            for page in range(pages):
                future = executor.submit(self._search_page, query, page, engine_config)
                futures.append(future)

            for future in as_completed(futures):
                try:
                    page_results = future.result()
                    all_results.extend(page_results)
                except Exception as e:
                    log(f"Erreur page: {e}", "ERROR")

        # Déduplication
        seen = set()
        unique_results = []
        for r in all_results:
            if r["url"] not in seen:
                seen.add(r["url"])
                unique_results.append(r)

        # Score de pertinence
        query_lower = query.lower()
        for r in unique_results:
            score = 0
            title_lower = r.get("title", "").lower()
            snippet_lower = r.get("snippet", "").lower()
            if query_lower in title_lower:
                score += 10
            if query_lower in snippet_lower:
                score += 5
            for word in query_lower.split():
                if word in title_lower:
                    score += 3
                if word in snippet_lower:
                    score += 1
            r["relevance"] = score

        unique_results.sort(key=lambda x: x.get("relevance", 0), reverse=True)

        if save_to_index:
            for r in unique_results:
                self.index.add_document(r["url"], r["title"], r["snippet"])

        self.results_cache[cache_key] = unique_results
        self.history.append({"query": query, "engine": self.engine, "time": datetime.now().isoformat(), "count": len(unique_results)})
        return unique_results

    def _search_page(self, query, page, engine_config):
        results = []
        try:
            params = {engine_config["param"]: query}
            if page > 0:
                params[engine_config["start"]] = page * engine_config["step"]

            if self.engine == "google":
                params.update({"hl": self.lang, "gl": self.country, "safe": self.safe_search})
            elif self.engine == "bing":
                params.update({"setlang": self.lang, "setmkt": f"{self.lang}-{self.country.upper()}"})
            elif self.engine == "yandex":
                params.update({"lr": self.country})

            response = self.session.get(
                engine_config["url"],
                params=params,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()

            if self.engine == "google":
                results = self._parse_google(response.text)
            elif self.engine == "bing":
                results = self._parse_bing(response.text)
            elif self.engine == "duckduckgo":
                results = self._parse_duckduckgo(response.text)
            elif self.engine == "yandex":
                results = self._parse_yandex(response.text)
            elif self.engine == "yahoo":
                results = self._parse_yahoo(response.text)
            elif self.engine == "brave":
                results = self._parse_brave(response.text)
            elif self.engine == "ecosia":
                results = self._parse_ecosia(response.text)

            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            log(f"Erreur moteur {self.engine}: {e}", "ERROR")
        return results

    def _parse_google(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for g in soup.find_all('div', class_=re.compile('g|tF2Cxc|Gx5Zad')):
            a = g.find('a', href=True)
            if not a or not a['href'].startswith('http'):
                continue
            title_tag = g.find('h3') or g.find('div', class_=re.compile('vvjwJb|VwiC3b'))
            snippet_tag = g.find('div', class_=re.compile('VwiC3b|s3v94d|lEBKkf'))
            results.append({
                "title": title_tag.get_text(strip=True) if title_tag else "Sans titre",
                "url": a['href'],
                "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
                "source": "Google",
            })
        return results

    def _parse_bing(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for li in soup.find_all('li', class_='b_algo'):
            a = li.find('a', href=True)
            if not a:
                continue
            snippet = li.find('p')
            results.append({
                "title": a.get_text(strip=True),
                "url": a['href'],
                "snippet": snippet.get_text(strip=True) if snippet else "",
                "source": "Bing",
            })
        return results

    def _parse_duckduckgo(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for result in soup.find_all('div', class_='result'):
            a = result.find('a', class_='result__a', href=True)
            if not a:
                continue
            snippet = result.find('a', class_='result__snippet')
            results.append({
                "title": a.get_text(strip=True),
                "url": a['href'],
                "snippet": snippet.get_text(strip=True) if snippet else "",
                "source": "DuckDuckGo",
            })
        return results

    def _parse_yandex(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for li in soup.find_all('li', class_=re.compile('serp-item|organic')):
            a = li.find('a', href=True)
            if not a or not a['href'].startswith('http'):
                continue
            title = li.find('h2') or li.find('a')
            snippet = li.find('div', class_=re.compile('text-container|organic__content-wrapper'))
            results.append({
                "title": title.get_text(strip=True) if title else "Sans titre",
                "url": a['href'],
                "snippet": snippet.get_text(strip=True) if snippet else "",
                "source": "Yandex",
            })
        return results

    def _parse_yahoo(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for div in soup.find_all('div', class_=re.compile('algo|Sr')):
            a = div.find('a', href=True)
            if not a:
                continue
            title = a.find('h3') or a
            snippet = div.find('p', class_=re.compile('fc-falcon|lh-24'))
            results.append({
                "title": title.get_text(strip=True),
                "url": a['href'],
                "snippet": snippet.get_text(strip=True) if snippet else "",
                "source": "Yahoo",
            })
        return results

    def _parse_brave(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for div in soup.find_all('div', class_=re.compile('snippet|result')):
            a = div.find('a', href=True)
            if not a or not a['href'].startswith('http'):
                continue
            title = div.find('span', class_=re.compile('title|heading'))
            snippet = div.find('div', class_=re.compile('description|desc'))
            results.append({
                "title": title.get_text(strip=True) if title else "Sans titre",
                "url": a['href'],
                "snippet": snippet.get_text(strip=True) if snippet else "",
                "source": "Brave",
            })
        return results

    def _parse_ecosia(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        for article in soup.find_all('article', class_='result'):
            a = article.find('a', href=True)
            if not a:
                continue
            title = article.find('h2')
            snippet = article.find('p', class_='snippet')
            results.append({
                "title": title.get_text(strip=True) if title else "Sans titre",
                "url": a['href'],
                "snippet": snippet.get_text(strip=True) if snippet else "",
                "source": "Ecosia",
            })
        return results

    def multi_engine_search(self, query, pages=1):
        log("Recherche multi-moteurs en parallèle...", "SEARCH")
        all_results = []
        engines = list(SEARCH_ENGINES.keys())
        with ThreadPoolExecutor(max_workers=len(engines)) as executor:
            futures = {}
            for engine in engines:
                temp_engine = TchadSearchEngine(engine=engine, lang=self.lang, country=self.country)
                future = executor.submit(temp_engine.search, query, pages, False)
                futures[future] = engine

            for future in as_completed(futures):
                engine = futures[future]
                try:
                    results = future.result()
                    for r in results:
                        r["source"] = engine.capitalize()
                    all_results.extend(results)
                    log(f"{engine.capitalize()}: {len(results)} résultats", "OK")
                except Exception as e:
                    log(f"Erreur {engine}: {e}", "ERROR")

        seen = set()
        unique_results = []
        for r in all_results:
            if r["url"] not in seen:
                seen.add(r["url"])
                unique_results.append(r)

        for r in unique_results:
            self.index.add_document(r["url"], r["title"], r["snippet"])
        return unique_results

    def image_search(self, query, pages=1):
        log(f"Recherche d'images: '{query}'", "SEARCH")
        results = []
        try:
            # Utilise DuckDuckGo images via html
            for page in range(pages):
                params = {
                    "q": query,
                    "ia": "images",
                    "iax": "images",
                }
                if page > 0:
                    params["s"] = page * 30
                response = self.session.get("https://duckduckgo.com/", params=params, timeout=self.timeout)
                soup = BeautifulSoup(response.text, 'html.parser')
                for img in soup.find_all('img', src=True):
                    src = img['src']
                    if src.startswith('http'):
                        results.append({
                            "title": img.get('alt', 'Image'),
                            "url": src,
                            "snippet": "",
                            "source": "DuckDuckGo Images",
                            "type": "image",
                        })
                time.sleep(0.5)
        except Exception as e:
            log(f"Erreur recherche images: {e}", "ERROR")
        return results

    def news_search(self, query, pages=1):
        log(f"Recherche d'actualités: '{query}'", "SEARCH")
        results = []
        try:
            for page in range(pages):
                params = {
                    "q": query,
                    "tbm": "nws",
                    "hl": self.lang,
                    "gl": self.country,
                }
                if page > 0:
                    params["start"] = page * 10
                response = self.session.get("https://www.google.com/search", params=params, timeout=self.timeout)
                soup = BeautifulSoup(response.text, 'html.parser')
                for g in soup.find_all('div', class_=re.compile('g|dbsr|xuvVjd')):
                    a = g.find('a', href=True)
                    if not a or not a['href'].startswith('http'):
                        continue
                    title = g.find('h3') or g.find('div', class_=re.compile('mCBkyc|nDgy9d'))
                    snippet = g.find('div', class_=re.compile('GI74Re|Y3fm8|st'))
                    results.append({
                        "title": title.get_text(strip=True) if title else "Sans titre",
                        "url": a['href'],
                        "snippet": snippet.get_text(strip=True) if snippet else "",
                        "source": "Google News",
                        "type": "news",
                    })
                time.sleep(0.5)
        except Exception as e:
            log(f"Erreur recherche news: {e}", "ERROR")
        return results

    def translate(self, text, target_lang="en"):
        log(f"Traduction vers {target_lang}...", "INFO")
        try:
            # LibreTranslate gratuit
            url = "https://libretranslate.de/translate"
            payload = {
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text"
            }
            response = self.session.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                return response.json().get("translatedText", "")
        except Exception as e:
            log(f"Erreur traduction: {e}", "ERROR")
        return None

    def weather_search(self, city):
        log(f"Météo pour: {city}", "SEARCH")
        try:
            # wttr.in
            url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current_condition", [{}])[0]
                return {
                    "city": city,
                    "temp_c": current.get("temp_C"),
                    "temp_f": current.get("temp_F"),
                    "condition": current.get("weatherDesc", [{}])[0].get("value"),
                    "humidity": current.get("humidity"),
                    "wind": current.get("windspeedKmph"),
                }
        except Exception as e:
            log(f"Erreur météo: {e}", "ERROR")
        return None

    def ip_info(self):
        log("Obtention des informations IP...", "INFO")
        try:
            response = self.session.get("https://ipapi.co/json/", timeout=10)
            return response.json()
        except Exception as e:
            log(f"Erreur IP info: {e}", "ERROR")
        return None

    def save_history(self):
        history_file = os.path.join(self.index.index_dir, "history.json")
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        history_file = os.path.join(self.index.index_dir, "history.json")
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)

# ═══════════════════════════════════════════════════════════════════
# INTERFACE UTILISATEUR
# ═══════════════════════════════════════════════════════════════════
def display_results(results, start=0, per_page=10):
    if not results:
        log("Aucun résultat trouvé", "WARN")
        return

    end = min(start + per_page, len(results))
    print(f"\n{Colors.CYAN}{Colors.BOLD}═══ Résultats {start+1} à {end} sur {len(results)} ═══{Colors.RESET}\n")

    for i, r in enumerate(results[start:end], start=start+1):
        source_color = Colors.MAGENTA
        print(f"{Colors.YELLOW}{Colors.BOLD}[{i}]{Colors.RESET} {Colors.GREEN}{Colors.BOLD}{r.get('title', 'Sans titre')}{Colors.RESET}")
        print(f"    {Colors.BLUE}{r.get('url', '')}{Colors.RESET}")
        print(f"    {Colors.WHITE}{r.get('snippet', '')[:250]}{Colors.RESET}")
        print(f"    {source_color}[Source: {r.get('source', 'Inconnue')} | Pertinence: {r.get('relevance', 0)}]{Colors.RESET}\n")

def show_help():
    print(f"""
{Colors.CYAN}{Colors.BOLD}Commandes disponibles :{Colors.RESET}
  /help              Afficher cette aide
  /engines           Liste des moteurs de recherche
  /engine <nom>      Changer de moteur (google, bing, yandex, ...)
  /multi <requête>   Recherche multi-moteurs
  /images <requête>  Rechercher des images
  /news <requête>    Rechercher des actualités
  /translate <texte> Traduire un texte
  /weather <ville>   Météo d'une ville
  /ip                Informations IP
  /history           Historique des recherches
  /local <requête>   Recherche dans l'index local
  /save              Sauvegarder l'historique
  /quit              Quitter
""")

def interactive_mode(engine):
    clear()
    banner()
    search_engine = TchadSearchEngine(engine=engine)
    search_engine.load_history()

    print(f"\n{Colors.GREEN}Moteur actuel: {engine.upper()} | Langue: {LANGUAGES.get(engine, 'Français')}{Colors.RESET}")
    print(f"{Colors.YELLOW}Tapez /help pour voir les commandes{Colors.RESET}\n")

    current_results = []
    current_page = 0

    while True:
        try:
            user_input = input(f"{Colors.CYAN}[TCHAD-SEARCH]{Colors.RESET} {Colors.YELLOW}> {Colors.RESET}").strip()
            if not user_input:
                continue

            if user_input.lower() == "/quit":
                search_engine.save_history()
                log("Au revoir !", "INFO")
                break
            elif user_input.lower() == "/help":
                show_help()
            elif user_input.lower() == "/engines":
                print(f"{Colors.CYAN}Moteurs disponibles:{Colors.RESET}")
                for e in SEARCH_ENGINES:
                    marker = " ← actuel" if e == search_engine.engine else ""
                    print(f"  - {e.upper()}{marker}")
            elif user_input.lower().startswith("/engine "):
                new_engine = user_input.split(" ", 1)[1].strip().lower()
                if search_engine.set_engine(new_engine):
                    log(f"Moteur changé pour {new_engine.upper()}", "OK")
                else:
                    log("Moteur inconnu", "ERROR")
            elif user_input.lower().startswith("/multi "):
                query = user_input.split(" ", 1)[1]
                current_results = search_engine.multi_engine_search(query, pages=1)
                current_page = 0
                display_results(current_results)
            elif user_input.lower().startswith("/images "):
                query = user_input.split(" ", 1)[1]
                results = search_engine.image_search(query)
                display_results(results)
            elif user_input.lower().startswith("/news "):
                query = user_input.split(" ", 1)[1]
                results = search_engine.news_search(query)
                display_results(results)
            elif user_input.lower().startswith("/translate "):
                text = user_input.split(" ", 1)[1]
                translated = search_engine.translate(text)
                if translated:
                    print(f"{Colors.GREEN}Traduction: {translated}{Colors.RESET}")
                else:
                    log("Traduction échouée", "ERROR")
            elif user_input.lower().startswith("/weather "):
                city = user_input.split(" ", 1)[1]
                weather = search_engine.weather_search(city)
                if weather:
                    print(f"{Colors.CYAN}Météo {weather['city']}: {weather['temp_c']}°C, {weather['condition']}, Humidité {weather['humidity']}%{Colors.RESET}")
                else:
                    log("Météo indisponible", "ERROR")
            elif user_input.lower() == "/ip":
                info = search_engine.ip_info()
                if info:
                    print(f"{Colors.CYAN}IP: {info.get('ip')} | Pays: {info.get('country_name')} | Ville: {info.get('city')} | FAI: {info.get('org')}{Colors.RESET}")
                else:
                    log("Infos IP indisponibles", "ERROR")
            elif user_input.lower() == "/history":
                for h in search_engine.history[-20:]:
                    print(f"{Colors.DIM}{h['time']}{Colors.RESET} | {Colors.YELLOW}{h['query']}{Colors.RESET} ({h['engine']}, {h['count']} résultats)")
            elif user_input.lower().startswith("/local "):
                query = user_input.split(" ", 1)[1]
                results = search_engine.index.search(query)
                display_results(results)
            elif user_input.lower() == "/save":
                search_engine.save_history()
                log("Historique sauvegardé", "OK")
            elif user_input.lower() in ["/next", "/page"]:
                if current_results:
                    current_page += 10
                    display_results(current_results, start=current_page)
                else:
                    log("Aucun résultat à afficher", "WARN")
            else:
                current_results = search_engine.search(user_input, pages=1)
                current_page = 0
                display_results(current_results)
        except KeyboardInterrupt:
            print()
            search_engine.save_history()
            break
        except Exception as e:
            log(f"Erreur: {e}", "ERROR")

# ═══════════════════════════════════════════════════════════════════
# MODE LIGNE DE COMMANDE
# ═══════════════════════════════════════════════════════════════════
def cli_mode(args):
    engine = TchadSearchEngine(engine=args.engine, lang=args.lang, country=args.country)

    if args.multi:
        results = engine.multi_engine_search(args.query, pages=args.pages)
    elif args.images:
        results = engine.image_search(args.query, pages=args.pages)
    elif args.news:
        results = engine.news_search(args.query, pages=args.pages)
    elif args.weather:
        info = engine.weather_search(args.query)
        print(json.dumps(info, indent=2, ensure_ascii=False) if info else "Erreur")
        return
    elif args.ip:
        info = engine.ip_info()
        print(json.dumps(info, indent=2, ensure_ascii=False) if info else "Erreur")
        return
    else:
        results = engine.search(args.query, pages=args.pages)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        display_results(results)

# ═══════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} v{VERSION}")
    parser.add_argument("-q", "--query", help="Requête de recherche")
    parser.add_argument("-e", "--engine", default="duckduckgo", choices=list(SEARCH_ENGINES.keys()), help="Moteur de recherche")
    parser.add_argument("-l", "--lang", default="fr", help="Code langue")
    parser.add_argument("-c", "--country", default="fr", help="Code pays")
    parser.add_argument("-p", "--pages", type=int, default=1, help="Nombre de pages")
    parser.add_argument("--multi", action="store_true", help="Recherche multi-moteurs")
    parser.add_argument("--images", action="store_true", help="Recherche d'images")
    parser.add_argument("--news", action="store_true", help="Recherche d'actualités")
    parser.add_argument("--weather", action="store_true", help="Météo")
    parser.add_argument("--ip", action="store_true", help="Infos IP")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    args = parser.parse_args()

    if args.query or args.ip:
        cli_mode(args)
    else:
        interactive_mode(args.engine)

if __name__ == "__main__":
    main()
