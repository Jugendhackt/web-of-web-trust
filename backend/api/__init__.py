from api.db import db
from api.db.config import API_SSL
from api.domains.routes import domain_router
from api.ruegen.routes import ruegen_router
from api.utility.routes import utility_router
from fastapi import FastAPI

api_description = """
The web of web trust backend. Making the web a bit more assessable ⚖️

## Idea

The current web is filled with valuable information and can help you in informing yourself.
But when informing oneself, you might quickly find out that assessing information and distinguishing between facts and disinformation can be increasingly hard, especially when researching a controversial or political topic.

To help with tackling this problem, [we](https://github.com/orgs/Jugendhackt/teams/web-of-web-trust) have gone back to the roots of the first search engines and thought about an easy-to-use but informative way of giving the user insight in the reputability of a website.
Similar to the first search engines, like yahoo, we assess websites based on the number of times there are linked by other websites and how many times they link to external websites. This method in itself is simple and doesn't really provide a good way of assessing sources, though.

And that's where our special sauce comes into play. By having a seed set for both factual news and misinformative news sites, we can build two networks describing the above-mentioned method. We can use these networks to evaluate a score and present it to the user.
We can then supplement the data with metadata about e.g. topicality and also, since we have the full index, sites that link to the current website. This allows the user to gain deeper insight in the trust between websites and allows us to build a web-of-web-trust that provides explainability and transparency for scores.
We also want, (WIP), to allow the user to set their own weights in the composition of the score to allow for a more personalized scoring.

## End-Product and Architecture

We plan to realize our idea in the form of a browser extension that allows the user to have immediate feedback when visiting a new site.

> See our current [`progress`](https://github.com/Jugendhackt/web-of-web-trust-client)

## Privacy-First Design

> Thanks to [e1mo](https://github.com/e1mo) and [em0lar](https://github.com/em0lar) we also have a privacy first design for information fetching by clients. 

### Why is a special design even needed? 

Since all clients, such as the browser extension, will be fetching a website that the user currently visits it would be easy for a malicious operator to track all users.

To mitigate this thread clients *must* request domains, and ruegen, by the first chars of a [BLAKE3](https://github.com/BLAKE3-team/BLAKE3) [hexdigest](https://docs.python.org/3/library/hashlib.html#hashlib.hash.hexdigest) of the FQDN.
The API will then return all domains that start with the supplied characters in a paginated manner.
By using this technique the server may not know the specifc request domain.

> This will also over time make the reversing of hash -> FQDn harder, since domains in the database will grow.

## Structure

### Domains

Domains are websites identified by a [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) and accessed by a sha-1 hexdigest of the FQDN. Domains are indexed by `Scrapers` that find a domain by scraping the base-set of domains for each network.

### Ruegen

We offer a collection of pre-sorted [„Presserügen“](https://de.wikipedia.org/wiki/Deutscher_Presserat), a notice of a defect in a publication for german newspapers. 

This collection is connected with the respective domains for the newspapers and are fetchable by the same pattern as domains.

## Credits

Original Developers from Jugendhackt Berlin 2021:

- Cobalt – [GitLab](https://gitlab.cobalt.rocks/cobalt/) [Website](https://cobalt.rocks)
- e1mo – [GitHub](https://github.com/e1mo)
- em0lar – [GitHub](https://github.com/em0lar) [Website](https://em0lar.de/)
- funi0n – [GitHub](https://github.com/funi0n)
- NecnivlixAlpaka – [GitHub](https://github.com/NecnivlixAlpaka)
- Schmensch – [GitHub](https://github.com/Schmensch)
- smyril42 – [GitHub](https://github.com/smyril42)
- Vincent – [GitHub](https://github.com/alpakathrowaway)
- Wolfaround - [GitHub](https://github.com/Wolfaround)

And our mentor:

- pajowu - [GitHub](https://github.com/pajowu) [Website](https://pajowu.de/)

## License

The backend is licensed under the AGPL-3-only license
"""

api = FastAPI(
    title="web-of-web-trust-backend",
    description=api_description,
    version="0.1.1b0",
    docs_url="/docs",
    redoc_url=None,
    contact={
        "name": "Cobalt",
        "url": "http://cobalt.rocks/",
        "email": "c0balt@disroot.org",
    },
    license_info={
        "name": "AGPL 3.0 (only)",
        "url": "https://www.gnu.org/licenses/agpl-3.0.txt",
    },
)
db.init_app(api)
api.include_router(domain_router)
api.include_router(ruegen_router)
api.include_router(utility_router)
