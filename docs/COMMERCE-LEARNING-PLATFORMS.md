# Commerce and e-learning platform analysis — 2026-11-24

Source: the two platform taxonomies supplied by the user. These are public
market maps, not REA studies. Nothing here is a dependency; all integrations
stay optional and free-by-default.

## 1. Centralised commerce (seller pays fees, platform controls rules/payments)

| Segment | Platforms | Fit for a solo AI-run business |
|---|---|---|
| Global B2C/B2B | Amazon, eBay, Alibaba/Alibaba.com, AliExpress, Temu, Shein | Large reach, high fees and strict rules; list products via API only if the person has an account |
| UK/EU | OnBuy, Argos, Currys, Zalando, ASOS | OnBuy is notable because it does not compete with its own sellers |
| Niche/secondhand | Etsy, Vinted, Depop, StockX | Good for handmade, secondhand and authenticated collectibles |
| B2B wholesale | Faire, Ankorstore | Matches a business that manufactures or sources goods |

**Build decision:** model these as `COMMERCE_CHANNELS` metadata with
`requiresOwnAccount: true`. The app never holds marketplace credentials; the
person connects their own account via the bridge/OAuth. Fees stay with the
platform; no feature in Polsia Free v1 is unlocked by listing on any of them.

## 2. Decentralised commerce (Web3, peer-to-peer, crypto payments)

| Segment | Platforms | Notes |
|---|---|---|
| P2P physical/digital | Particl (PART, two-party escrow), Syscoin/Blockmarket, BitBay (double-deposit escrow) | Escrow replaces the intermediary; keys are the user's |
| Commerce protocols | Boson Protocol (redeemable rNFTs), Origin/Dshop (IPFS storefronts), Request Network/Slasify (crypto invoicing) | Request Network aligns with our invoice/receipt model |
| NFT/digital goods | OpenSea, Blur, Rarible | Non-custodial wallets; minting/trading needs the person's wallet |
| Historic | OpenBazaar (shut down) | Proof of zero-fee P2P commerce; not a current integration |

**Build decision:** record as `WEB3_COMMERCE` references. Our crypto invoice
and wallet-URI flow already covers the payment primitive; actual marketplace
actions need the person's own wallet and per-transaction approval. No NFT
minting is automated.

## 3. Centralised e-learning

| Segment | Platforms | Fit |
|---|---|---|
| Academic MOOCs | Coursera, edX, FutureLearn, Khan Academy | Free-first: **Khan Academy** is the strongest free source |
| Tech/coding | Pluralsight, DataCamp, Codecademy, Treehouse | Paid, but Codecademy/Treehouse have free tiers |
| Creative/business | LinkedIn Learning, MasterClass, Domestika | Paid subscriptions |

## 4. Decentralised / open e-learning

| Segment | Platforms | Fit |
|---|---|---|
| Open instructor markets | Udemy, Skillshare, Teachable/Kajabi/Thinkific, Outschool | Creator-hosted; quality varies by rating |
| Open-source communities | **freeCodeCamp, P2PU, Wikiversity** | Fully free; best match for our `SKILLS` registry |
| Web3 learn-to-earn | Open Campus (EDU), BitDegree, RabbitHole/Galxe | On-chain credentials/rewards; optional, keys required |

**Build decision:** add `LEARNING_SOURCES` with a **free-first ordering**:
freeCodeCamp, Khan Academy, Wikiversity, P2PU first; paid platforms listed as
optional. Local skill records stay in this browser; no NFT credential is
issued without the person's own wallet.

## Cross-cutting conclusions

1. Both markets split the same way: **centralised = convenience + fees +
   control; decentralised = custody + censorship resistance + key risk**.
2. For the solo business runner, the practical path is centralised
   marketplaces for reach, plus the app's own bridge for invoices/receipts and
   crypto where the customer opts in.
3. For learning, the free/open sources already cover most of what the team
   needs to self-improve; paid courses are optional inputs, never gates.
4. None of these platforms should be presented as "connected" until the person
   supplies their own credentials. The registries are reference data only.

## Verification note
Registered in `app/src/marketplaces.js` when the build is green; no code, logos
or course content from these platforms is copied.
