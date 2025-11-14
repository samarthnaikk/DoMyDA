import asyncio
import logging
import httpx
from typing import Optional

from .browser import open_browser
from .utils import extract_base64, extract_submit_url


async def compute_answer(page) -> str:
    """Placeholder answer computation. Replace with real logic.

    For now returns a dummy value.
    """
    # Example: evaluate something on the page if needed
    try:
        title = await page.title()
    except Exception:
        title = ""
    return "42"


async def solve_quiz(email: str, secret: str, start_url: str) -> None:
    """Main solve loop: navigates pages, extracts question/base64, computes answer, submits, follows next URL."""
    logging.info("Solver started for %s", email)
    p, browser, context, page = await open_browser()
    try:
        url: Optional[str] = start_url
        async with httpx.AsyncClient() as client:
            while url:
                logging.info("Loading page: %s", url)
                try:
                    await page.goto(url, wait_until="networkidle")
                except Exception:
                    logging.exception("Failed to load page %s", url)
                    break
                await asyncio.sleep(0.5)
                html = await page.content()
                # extract base64 or question
                b64 = extract_base64(html)
                if b64:
                    logging.info("Found base64 block (len=%d)", len(b64))
                try:
                    submit_url = extract_submit_url(html, url)
                except ValueError:
                    logging.exception("Submit URL not found; stopping")
                    break
                answer = await compute_answer(page)
                payload = {"email": email, "answer": answer}
                logging.info("Submitting answer to %s", submit_url)
                try:
                    resp = await client.post(submit_url, json=payload, timeout=30.0)
                except Exception:
                    logging.exception("Submission failed")
                    break
                try:
                    data = resp.json()
                except Exception:
                    logging.debug("Non-JSON response received; stopping")
                    break
                next_url = data.get("url")
                if not next_url:
                    logging.info("No next url in response; finishing")
                    break
                url = next_url
                await asyncio.sleep(1)
    finally:
        try:
            await context.close()
        except Exception:
            pass
        try:
            await browser.close()
        except Exception:
            pass
        try:
            await p.stop()
        except Exception:
            pass
    logging.info("Solver finished for %s", email)
