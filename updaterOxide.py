import os, aiohttp, asyncio, zipfile

OUTPUT_FILE = "rust_umod.zip"
TARGET_DIR = "rustds"

async def download_oxide():
    url = f"https://umod.org/games/rust/download?tag=public"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                print(f"[ERROR] status_code -> {resp.status}")
                return
            print(f"Скачиваю Oxide...")
            with open(OUTPUT_FILE, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return True

def unpack_oxide():
    os.makedirs(TARGET_DIR, exist_ok=True)
    with zipfile.ZipFile(OUTPUT_FILE, "r") as zip_ref:
        zip_ref.extractall(TARGET_DIR)
    print(f"Распакоувка...")

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

async def main():
    if await download_oxide():
        unpack_oxide()
        print("Oxide обновлён!")
        return

if __name__ == "__main__":
    asyncio.run(main())