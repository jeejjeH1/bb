# Per-project copy for the project pages. Written from each repo's README (or the video itself
# where the repo has none). Keys match the slugs in works.json.
META = {
 'many-minds': dict(
  sum="Why does GenLayer use several AI models instead of one? A 72-second explainer that follows one AI failing as a single point of failure, then a network of validators catching its mistakes.",
  beats=["The GenLayer logo draws itself and lands with a shockwave", "One AI chip hallucinates, gets prompt-injected and shatters", "Five validators evaluate the same decision", "Optimistic Democracy: propose, challenge, appeal, finalize"],
  stack=["Canvas animation", "Synthesized soundtrack", "Frame-by-frame render"]),
 'intelligent-contracts': dict(
  sum="Why GenLayer needs direct web access. A calm, minimal piece with a 3D cat-astronaut mascot and an extruded GenLayer logo, built for an X thread on intelligent contracts.",
  beats=["3D logo assembles", "The mascot lands and asks the question", "Contracts read the web and reason over it", "Soft word-by-word type, slow camera"],
  stack=["Three.js", "3D mascot", "FM piano and pad soundtrack", "Playwright render"]),
 'thread-of-light': dict(
  sum="The second cut of the Intelligent Contracts post: no character, only particles and a single thread of light that carries the idea from the chain to the open web.",
  beats=["Particle-only visual language", "A thread of light links contract and web", "Same script as v1, new mood"],
  stack=["Canvas particles", "Ambient soundtrack", "Playwright render"]),
 'appeals': dict(
  sum="An 80-second explainer on why the right to challenge a decision matters in GenLayer: what happens when an AI-powered contract gets it wrong, and how appeals bring in more validators.",
  beats=["“Why is the ability to challenge a decision important?”", "An AI contract accepts a result that may be wrong", "APPEALS lands as a neon glitch title", "Optimistic Democracy reviews the dispute"],
  stack=["Canvas render(t)", "Synthesized SFX and pad", "Playwright + ffmpeg"]),
 'roadmap': dict(
  sum="The road to GenLayer mainnet in 42 seconds: five milestones from the 2024 whitepaper through Asimov, Bradbury and Clarke to mainnet, each with its own date card.",
  beats=["“The road to mainnet” title", "Whitepaper, Asimov, Bradbury, Clarke", "Mainnet marked as the next milestone", "Timeline end card"],
  stack=["HTML animation", "Parallel frame render", "Synthesized soundtrack"]),
 'insurance': dict(
  sum="GenLayer applied to insurance: a flight-delay policy that pays out on its own, with intelligent contracts reading real-world data and validators agreeing on the result.",
  beats=["Insurance still runs on manual reviews", "Flight delay insurance, settled by contract", "Optimistic Democracy on the claim", "“What other industries could benefit?”"],
  stack=["Canvas animation", "120 BPM F-minor soundtrack", "Playwright render"]),
 'defi': dict(
  sum="Can the next generation of DeFi go beyond predefined rules? A clean, light-themed piece that contrasts rigid if/else contracts with a protocol that evaluates the real world.",
  beats=["“Can DeFi go beyond predefined rules?”", "A brittle settle() function fails on reality", "GenLayer intelligent contracts and Optimistic Democracy", "Challenges that remain: security, data, cost"],
  stack=["3D primitives", "Kinetic typography", "Synthesized soundtrack"]),
 'rally': dict(
  sum="Launch video for the GenLayer campaign on Rally: a live prize pool counter, three simple steps and a call to join with real content instead of farming.",
  beats=["GenLayer is live on Rally", "Total prize pool counts up to 100,000 GLP", "Join · Quote · Share", "“No farming. No copy-paste.”"],
  stack=["HTML animation", "Counter and UI motion", "Synthesized soundtrack"]),
 'internet-court': dict(
  sum="A 2:09 case study for the MetaMask × GenLayer Internet Court thread: an AI agent stays inside its budget and still does the wrong thing, so a decentralized jury decides.",
  beats=["3D fox, GenLayer and Internet Court logos", "18 scenes of UI mockups and kinetic type", "Jury simulation, appeals counter and verdicts", "A keyframed cursor drives every interaction"],
  stack=["Three.js logos", "Procedural 120 BPM score", "60 fps Playwright render"]),
 'genvm': dict(
  sum="A creepy, fur-and-glitch take on GenVM. A hundred cat eyes stop agreeing once contracts have to call an LLM or read a webpage, and the camera dives into a pupil to reveal GenVM.",
  beats=["Glowing cat eyes open under heavy glitch", "100 nodes blink in perfect sync", "Determinism breaks once reality enters", "“This is where GenVM becomes interesting.”"],
  stack=["Canvas + glitch post-FX", "Layered blink sound design", "60 fps render"]),
 'genvm-clean-cut': dict(
  sum="The same GenVM story told a completely different way: a premium keynote-style cut with Swiss-grid type, colour-block transitions and every cut on a 120 BPM beat.",
  beats=["“Blockchains love determinism. Reality doesn't.”", "100 tiles flip in sync, then disagree", "A cursor ticks on LLM, web and data", "Split screen: traditional vs intelligent contracts"],
  stack=["Kinetic typography", "Colour-block transitions", "Beat-synced soundtrack"]),
 'agent-economy': dict(
  sum="When two AI agents make a deal and disagree, who decides? A 55-second story from an agent shopping for you to a courthouse that collapses under millions of disputes, and GenLayer as the new trust layer.",
  beats=["A shop website dissolves into your AI agent", "Agent negotiates, signs and pays another agent", "The dispute: who decides?", "A new trust layer drops onto the stack"],
  stack=["Canvas animation", "Particles and 3D layers", "Synthesized soundtrack"]),
 'genlayer-motion': dict(
  sum="A 108-second piece on GenLayer as the judgment layer of the agentic economy, with a 3D network of about 2,200 agents and a vectorised GenLayer mark extruded in 3D.",
  beats=["An agent says TASK COMPLETE, then VERIFIED BY: ???", "3D stack with an empty judgment slot", "A 99.2%-confident answer stamped WRONG", "A ring of independent validators"],
  stack=["Three.js", "3D agent network", "60 fps render"]),
 'tee-explainer': dict(
  sum="What are Trusted Execution Environments? A 90-second Seismic explainer with a 3D rock golem, a leaking glass blockchain and shielded storage tiles, in light brown, cream and black.",
  beats=["Public chain of glass blocks leaking data", "The golem assembles and powers up", "Encrypted tx executed in Intel TDX", "Remote attestation rejects a rogue node"],
  stack=["Three.js scene", "DOM typography", "Original synthesized score"]),
 'ecosystem': dict(
  sum="The 11 fintechs already building on Seismic. Cut to a 120 BPM grid, with neobanks, payments, credit and AI finance introduced on each beat and the stablecoin stack explained.",
  beats=["“Neobanks. Payments. Credit. AI finance.”", "The Seismic mark assembles on the drop", "$17M raised, led by a16z crypto", "11 teams, one card each"],
  stack=["Canvas animation", "Beat grid shared with audio", "X-ready encodes"]),
 'stablecoin-stack': dict(
  sum="Stablecoins may not replace banks, they may become the infrastructure. A Seismic piece on the full stablecoin stack, private payroll on a public chain, and privacy without zero visibility.",
  beats=["“Not another token. A stablecoin stack.”", "A US company pays a contractor in India", "A chat explains why public payroll is a dealbreaker", "“Privacy ≠ zero visibility”"],
  stack=["Canvas animation", "Chat UI mockups", "Synthesized soundtrack"]),
 'startale-motion': dict(
  sum="Why is crypto adoption still hard, and how does Startale make it simple? A 79-second piece at 128 BPM with a cursor, pastel mesh, bubbles and a logo that assembles square by square.",
  beats=["The logo lands one square per beat", "COMPLEXITY behind warning tape", "A cursor walks through the fix", "Glitch, shake and flash on the hits"],
  stack=["Shared 128 BPM timeline", "Canvas renderer", "Synthesized score and SFX"]),
 'bond-jpysc': dict(
  sum="Startale Bond × JPYSC with a narrated voiceover: a Three.js scene with extruded logos, a 3D bond card and a 3D “5%”, with kinetic type synced to the script.",
  beats=["3D Startale and JPYSC logos", "A 3D bond card and 5% yield", "Traditional markets meet on-chain infrastructure", "Music ducks under the narration"],
  stack=["Three.js", "Kokoro TTS voiceover", "Deterministic headless capture"]),
 'heroes-live': dict(
  sum="Launch video for HEROES going live on the Startale App: gameplay highlights cut from a screen recording, wrapped in motion graphics, with rewards for the most active players.",
  beats=["HEROES is now live", "Gameplay highlights, rotated and cropped", "5 seasons of tactical 1v1s", "How HEROES rewards work"],
  stack=["Gameplay montage", "Python render", "Synthesized soundtrack"]),
 'pieverse-promo': dict(
  sum="Startale App × Pieverse: deposit $5 and meet your AI agent. A bright pastel promo with a fluffy cat character and a single, clear offer.",
  beats=["“$5.” lands with an RGB split", "Startale App × Pieverse lockup", "Meet your AI agent", "100 STAR points and 7 days of access"],
  stack=["2D motion", "Pastel gradient look", "Promo cut"]),
 'kast-motion': dict(
  sum="Bridging crypto and the real world: a 70-second KAST piece in the brand's black, white and mint, covering payments, stablecoins, global money and a single “Pay” tap.",
  beats=["“How do we bridge the gap?”", "On-chain and real world, and a bridge that breaks", "KAST logo reveal on the drop", "Four pillars, then the card lineup"],
  stack=["Canvas animation", "Vector K mark", "Procedural score"]),
 'kast-latam-0fx': dict(
  sum="0% FX fees are now live across LATAM. A 22-second announcement in square and 16:9, with a slot-machine 0%, a dot-matrix map of Latin America and a card that waives the fee.",
  beats=["A digit reel slams onto 0%", "The LATAM map lights up north to south", "KAST FX fee: waived", "Available through 31 December 2027"],
  stack=["Canvas timeline", "Natural Earth map data", "-14 LUFS master"]),
 'what-is-fomies': dict(
  sum="What is @FomiesNFT? A tour of the Department of FOMO: an NFT collection built around a fictional government office, with corridors, a boarded door and WINDOW 3.",
  beats=["A case file is typed and stamped", "Walk the corridor, the elevator is under repair", "Ring the bell, take number 042", "“Always early. Always watching.”"],
  stack=["Canvas animation", "Typewriter and stamp SFX", "60 fps render"]),
 'prismax-iros-2026': dict(
  sum="PrismaX at IROS 2026 in Pittsburgh: a 40-second brand piece built from event photos, with bronze slats from the booth wall, the tech talk, the teleop rig and the numbers.",
  beats=["The service layer for physical AI", "Tech talk at 3:15 PM", "Teleop rig with detection boxes", "5,000 hrs/month · 120K+ episodes"],
  stack=["Photo-based motion", "Beat-synced soundtrack", "Brand kit from booth photos"]),
}
