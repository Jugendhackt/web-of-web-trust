# Web of Web Trust Backend

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

> See `/docs` fo your instance for an easy-to read OpenAPI spec

### Architecture

<div style="display: flex; justify-content: center;">

[![](https://mermaid.ink/svg/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBDKENsaWVudCkgLS0-fEZldGNoIGJ5IEhhc2h8IEJbQmFja2VuZF1cbiAgICBCIC0tPnxHcmFwaCBEYXRhfCBQW1Bvc3RncmVTUUxdXG4gICAgUCAtLT58RG9tYWlucyAmIFJ1ZWdlbnwgQlxuICAgIEIgLS0-fENhY2hlfCBSW1JlZGlzXVxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRhcmsiLCJ0aGVtZVZhcmlhYmxlcyI6eyJiYWNrZ3JvdW5kIjoidHJhbnNwYXJlbnQifX0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggVERcbiAgICBDKENsaWVudCkgLS0-fEZldGNoIGJ5IEhhc2h8IEJbQmFja2VuZF1cbiAgICBCIC0tPnxHcmFwaCBEYXRhfCBQW1Bvc3RncmVTUUxdXG4gICAgUCAtLT58RG9tYWlucyAmIFJ1ZWdlbnwgQlxuICAgIEIgLS0-fENhY2hlfCBSW1JlZGlzXVxuIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRhcmtcIixcbiAgXCJ0aGVtZVZhcmlhYmxlc1wiOiB7XG4gICAgICBcImJhY2tncm91bmRcIjogXCJ0cmFuc3BhcmVudFwiXG4gIH1cbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

</div>

### Domains

Domains are websites identified by a [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) and accessed by a sha-1 hexdigest of the FQDN. Domains are indexed by `Scrapers` that find a domain by scraping the base-set of domains for each network.

### Ruegen

We offer a collection of pre-sorted [„Presserügen“](https://de.wikipedia.org/wiki/Deutscher_Presserat), a notice of a defect in a publication for german newspapers. This collection is connected with the respective domains for the newspapers and are fetchable by the same privacy-first pattern as domains.

## Credits

Original Developers from [Jugendhackt Berlin 2021](https://jugendhackt.org/):

- Cobalt – [GitLab](https://gitlab.cobalt.rocks/cobalt/) | [Website](https://cobalt.rocks)
- e1mo – [GitHub](https://github.com/e1mo)
- em0lar – [GitHub](https://github.com/em0lar) | [Website](https://em0lar.de/)
- funi0n – [GitHub](https://github.com/funi0n)
- NecnivlixAlpaka – [GitHub](https://github.com/NecnivlixAlpaka)
- Schmensch – [GitHub](https://github.com/Schmensch)
- smyril42 – [GitHub](https://github.com/smyril42)
- Vincent – [GitHub](https://github.com/alpakathrowaway)
- Wolfaround – [GitHub](https://github.com/Wolfaround)

And our mentor:

- pajowu – [GitHub](https://github.com/pajowu) | [Website](https://pajowu.de/)

## License

The backend is licensed under the AGPL-3 (only) license by Cobalt \<https://cobalt.rocks\>.

Please refer to the licenses of the other parts of this project for their respective licenses.
