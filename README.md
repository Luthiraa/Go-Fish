# Welcome to Go Fish 🐟: Information in Reel 🎣 Time

## Motivation

Large language models and search engines often find non-relevant information, making them less useful in isolated environments (i.e. for individual companies). What if you could find more useful information, faster?

## How It Works
Go Fish combines API calls to relevant platforms with Groq’s fine-tuned LLM - instead of trying to find information on the entire internet, limit your search to information pulled directly from Shopify, StackOverflow, and more - you can even display code snippets pulled directly from Github!

After retrieving information via API calls, data is passed to Groq's LLM, where it filters and retrieves the information most relevant to your query.

Go Fish also emphasizes important terms and ideas within your search - making your search more relevant, more accurate, and more efficient.

## Cool Features
- Code snippet and specific linedisplay during Github search,
- Results summary display,
- Shopify search,
- Provides links to additional resources,
- In-line reddit post display,
- And more!

## How It's Better
Go Fish avoids some of the biggest problem with LLMs today. Many LLMs, including OpenAI (ChatGPT) both crawl the entire internet - leading to spider problems - and retrieve previously AI-generated information, leading to "AI inbreeding".

By restricting Go Fish's information to data retrieved via API call from human sources, your information is more relevant and more accurate, without falling victim to these common problems.

In addition, Go Fish can be expanded to store several of your last searches so you can quickly and easily return to previous information in air-gapped or internet-less environments. Go Fish's concept can also be applied to closed networks or information systems without global internet access for developers or employees.

## Uses and Applications
- Easy communication between software developers and those outside of programming spaces - relevant summaries, images, and linked resources give you the communication tools you need to make sure everyone is on board with your project.
- Bug fixing made easy - search your Github and return code snippets and specific lines.
- Need outside help? Interface with StackOverflow or Reddit to get answers you need - when in doubt, turn to outside experts.
- Adapt Go Fish to any search domain - here, we're demo-ing an expanded search space across Shopify, Reddit, and more, but it's easy to modify Go Fish to any interface - even local networks or employer-specific applications.

## How We Built It
Go Fish was created using **Javascript, React, and Python**, in combination with the following services and platforms:
- Groq (LLM)
- Shopify (API)
- Slack (API)
- Github (API)
- StackOverflow (API)
- GoDaddy (Domain)

## Future Applications and Considerations
Go Fish can be modified and applied to individual systems, e.g. for employees to use in workspaces - retrieving only useful information, and making work more efficient. Or: to any finite domain!

Go Fish is compatible with air-gapped (internet-less) practices of holding several recent searches in a queue, depending on data storage and retrieval needs, as well as required system size.

## Other useful links
- [Github](https://github.com/Luthiraa/Go-Fish)
- [GoFish.wiki](http://gofish.wiki/)
- [Presentaion](https://docs.google.com/presentation/d/1L-ce0wTBOxdkm2LJwvT0z2leot5CT0BwwbkEzPCmRYg/edit#slide=id.p)
