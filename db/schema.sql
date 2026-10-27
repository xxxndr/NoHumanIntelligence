-- Schema NoHumanIntelligence (PostgreSQL 18: uuidv7() nativo)
-- Ogni tabella figlia porta tenant_id; le FK composite (tenant_id, id) impediscono
-- di collegare righe di tenant diversi. La RLS arriva al punto 9.1.

BEGIN;

CREATE TYPE plan AS ENUM ('free', 'starter', 'pro');
CREATE TYPE conversation_status AS ENUM ('open', 'escalated', 'closed');
CREATE TYPE message_role AS ENUM ('user', 'assistant', 'operator', 'tool');
CREATE TYPE order_status AS ENUM ('placed', 'paid', 'shipped', 'delivered', 'cancelled');
CREATE TYPE ticket_status AS ENUM ('open', 'pending', 'resolved');

CREATE TABLE tenants (
    id         uuid        PRIMARY KEY DEFAULT uuidv7(),
    name       text        NOT NULL CHECK (length(name) BETWEEN 1 AND 200),
    plan       plan        NOT NULL DEFAULT 'free',
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE documents (
    id         uuid        PRIMARY KEY DEFAULT uuidv7(),
    tenant_id  uuid        NOT NULL REFERENCES tenants ON DELETE CASCADE,
    title      text        NOT NULL,
    version    integer     NOT NULL DEFAULT 1 CHECK (version > 0),
    metadata   jsonb       NOT NULL DEFAULT '{}' CHECK (jsonb_typeof(metadata) = 'object'),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, id),
    UNIQUE (tenant_id, title, version)
);
CREATE INDEX documents_metadata_idx ON documents USING gin (metadata jsonb_path_ops);

CREATE TABLE conversations (
    id           uuid                PRIMARY KEY DEFAULT uuidv7(),
    tenant_id    uuid                NOT NULL REFERENCES tenants ON DELETE CASCADE,
    status       conversation_status NOT NULL DEFAULT 'open',
    escalated_at timestamptz,
    created_at   timestamptz         NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, id),
    CHECK ((status = 'escalated') = (escalated_at IS NOT NULL))
);
CREATE INDEX conversations_tenant_status_idx ON conversations (tenant_id, status, created_at DESC);

CREATE TABLE messages (
    id              uuid         PRIMARY KEY DEFAULT uuidv7(),
    tenant_id       uuid         NOT NULL,
    conversation_id uuid         NOT NULL,
    role            message_role NOT NULL,
    content         text         NOT NULL,
    meta            jsonb        NOT NULL DEFAULT '{}' CHECK (jsonb_typeof(meta) = 'object'),
    created_at      timestamptz  NOT NULL DEFAULT now(),
    FOREIGN KEY (tenant_id, conversation_id)
        REFERENCES conversations (tenant_id, id) ON DELETE CASCADE
);
-- uuidv7 è ordinabile nel tempo: (conversation_id, id) legge i messaggi in ordine
CREATE INDEX messages_conversation_idx ON messages (conversation_id, id);

CREATE TABLE orders (
    id             uuid         PRIMARY KEY DEFAULT uuidv7(),
    tenant_id      uuid         NOT NULL REFERENCES tenants ON DELETE CASCADE,
    external_ref   text         NOT NULL,
    customer_email text         NOT NULL,
    status         order_status NOT NULL DEFAULT 'placed',
    total_cents    integer      NOT NULL CHECK (total_cents >= 0),
    placed_at      timestamptz  NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, external_ref)
);
CREATE INDEX orders_customer_idx ON orders (tenant_id, lower(customer_email));

CREATE TABLE tickets (
    id              uuid          PRIMARY KEY DEFAULT uuidv7(),
    tenant_id       uuid          NOT NULL,
    conversation_id uuid,
    subject         text          NOT NULL,
    status          ticket_status NOT NULL DEFAULT 'open',
    created_at      timestamptz   NOT NULL DEFAULT now(),
    FOREIGN KEY (tenant_id, conversation_id)
        REFERENCES conversations (tenant_id, id) ON DELETE SET NULL (conversation_id)
);
CREATE INDEX tickets_open_idx ON tickets (tenant_id, created_at DESC) WHERE status <> 'resolved';

COMMIT;
