# 🐛 Snake Game

A classic snake game built as a single HTML file — no install, no build step.
Just open `index.html` in any browser and play.

> **Project #2** for my AI agent class, where we learn to build websites, games, and
> other software by working with **Claude Code** as an AI coding agent.

## Play

**[▶ Live demo](https://jeminana.github.io/ERICA_X_MODULABS_CV/03_Seminar_1/snake_game/)**
*(enable GitHub Pages in Settings → Pages → Branch: `main` / root)*

Or clone and open locally:

```bash
git clone https://github.com/Jeminana/ERICA_X_MODULABS_CV.git
cd ERICA_X_MODULABS_CV/03_Seminar_1/snake_game
# then just open index.html in your browser
```

## Controls

| Key | Action |
|---|---|
| `↑` `↓` `←` `→` or `W` `A` `S` `D` | Move |
| `Space` | Pause / resume |
| `Space` or `Enter` | Restart after game over |

## Rules

- 20 × 20 grid, the snake moves 8 cells per second
- Start at the center with a length of 3, heading right
- Eating food: **+1 length, +10 points**, and new food spawns
- Game over when you hit a **wall** or **your own body**
- Reversing straight into yourself is ignored, not fatal

## Built With

- HTML5 Canvas + vanilla JavaScript — no libraries, no dependencies
- A single `index.html` containing markup, styles, and game logic

## How It Was Made

This project was built with **Claude Code** using a spec-driven workflow:

1. **Plan mode** — wrote a PRD first (game rules, screen layout, scope) and got it
   approved before any code was written
2. **Implementation** — built the game from that spec in one pass
3. **Work log** — every step was tracked and checked off in [`TODO.md`](TODO.md)
4. **Testing** — ran the game in the browser and verified each rule

Two bugs worth noting that the plan caught ahead of time:

- **Double-turn death** — pressing two direction keys within a single tick could turn
  the snake into its own neck. Fixed by queueing input in `nextDirection` and only
  committing it at the start of `step()`.
- **Phantom tail collision** — the tail cell moves away on the same tick, so it is
  excluded from collision checks unless the snake just ate.

## Files

| File | Purpose |
|---|---|
| `index.html` | The entire game (HTML + CSS + JS) |
| `TODO.md` | Development checklist and work log |
| `README.md` | This file |

## Ideas for Later

- [ ] Save high score with `localStorage`
- [ ] Speed increase / bonus food as the score grows
- [ ] Touch swipe controls for mobile + sound effects
