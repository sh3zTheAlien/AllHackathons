# REST API Contract

Base path `/api`. JSON in/out. ISO 8601 dates. Errors returned as `{ "error": string }` with the appropriate HTTP status code. CORS enabled for the frontend origin.

## Data Model

```typescript
interface Hackathon {
  id: string
  name: string            // REQUIRED; renamed from `topic`
  description?: string
  url?: string            // official link; renamed from `link`. For low-friction submits this may be the ONLY field provided
  startDate?: string      // ISO 8601 date; replaces the single `date` field
  endDate?: string        // ISO 8601 date
  location?: string       // free text city/venue
  mode?: "in-person" | "online" | "hybrid"
  organizer?: string
  hasPrize?: boolean      // replaces `prize`
  prizeDetails?: string
  tags?: string[]
  status: "draft" | "pending" | "published" | "needs-changes"
  submittedAt?: string    // ISO timestamp
  updatedAt?: string      // ISO timestamp
  interestCount?: number  // reserved; populated later via Discord (deferred)
  discordChannelId?: string // reserved; per-hackathon Discord channel/thread id (deferred)
}
```

### Submission rule

Only **one of `{ name, url }`** is required; everything else is optional.

### Empty-string normalization

Optional string fields normalize `""` to omitted (notably `location`). Both backend and frontend should treat `""` as absent.

## Status Lifecycle

| Status | Meaning |
|---|---|
| `draft` | Not yet submitted (local save) |
| `pending` | Submitted, awaiting admin review |
| `published` | Visible to everyone (auto-published or approved) |
| `needs-changes` | Changes requested by admin |

**Flow:**
1. Submit → AI validation → `"published"` (auto, the default happy path) **or** `"pending"` (if validation flags the submission).
2. Admins review `pending` / `needs-changes` items periodically.
3. A change request against a `published` item creates a separate `"needs-changes"` pending edit. The live published item is **untouched** until an admin (or AI) approves the edit.

## Endpoints

### Hackathons

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/hackathons` | List published. Query: `?status=` `&upcoming=true` `&past=true` `&tag=` `&q=` `&sort=date` |
| `GET` | `/api/hackathons/:id` | Single hackathon |
| `POST` | `/api/hackathons` | Submit new (`name` OR `url` required); runs AI validation; returns created resource + status |
| `PATCH` | `/api/hackathons/:id` | Edit fields |
| `POST` | `/api/hackathons/:id/change-request` | Request changes to a published hackathon (creates a reviewable pending edit) |

### Q&A

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/hackathons/:id/questions` | List Q&A |
| `POST` | `/api/hackathons/:id/questions` | Post a question |
| `POST` | `/api/questions/:id/answers` | Answer a question |

### Interest (deferred)

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/hackathons/:id/interest` | Interest count |

## Endpoint Ownership

| Owner | Endpoints |
|---|---|
| `backend-api` | `GET/POST/PATCH /api/hackathons`, `GET /api/hackathons/:id`, `POST /api/hackathons/:id/change-request` |
| `qa-comments` | `GET/POST /api/hackathons/:id/questions`, `POST /api/questions/:id/answers` |
| `discord-interest` | `GET /api/hackathons/:id/interest` |

Each endpoint has exactly **one** server-side owner.

## Conventions

- **Transport:** JSON request and response bodies.
- **Dates:** ISO 8601 throughout (`startDate`, `endDate`, `submittedAt`, `updatedAt`).
- **Errors:** `{ "error": string }` with a correct HTTP status (e.g. `400` validation, `404` not found, `422` unprocessable).
- **CORS:** enabled for the frontend origin so the React app can call the API in the browser.
- **Empty strings:** optional string fields normalize `""` to omitted (notably `location`).
