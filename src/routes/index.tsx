import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import {
  Activity,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  Check,
  ChevronDown,
  CircleHelp,
  Clock3,
  Inbox,
  Layers3,
  LifeBuoy,
  Menu,
  MessageSquareText,
  MoreHorizontal,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  UsersRound,
  Workflow,
  X,
  Zap,
} from "lucide-react";

import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "SupportPilot — Customer support, in sync" },
      {
        name: "description",
        content:
          "Bring every customer conversation, teammate, and next step together in one thoughtful support workspace.",
      },
      { property: "og:title", content: "SupportPilot — Customer support, in sync" },
      {
        property: "og:description",
        content:
          "A clearer workspace for customer conversations, team handoffs, and thoughtful support.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  const [menuOpen, setMenuOpen] = useState(false);

  const closeMenu = () => setMenuOpen(false);

  return (
    <main className="min-h-screen overflow-hidden bg-background text-foreground">
      <header className="sticky top-0 z-40 border-b border-border/70 bg-background/95 backdrop-blur">
        <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between gap-5 px-5 sm:px-8">
          <a className="flex shrink-0 items-center gap-3" href="#top" aria-label="SupportPilot home">
            <span className="flex size-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <LifeBuoy aria-hidden="true" className="size-5" />
            </span>
            <span className="font-display text-xl font-bold">SupportPilot</span>
          </a>

          <nav aria-label="Main navigation" className="hidden items-center gap-8 md:flex">
            <a className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground" href="#product">Product</a>
            <a className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground" href="#features">Features</a>
            <a className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground" href="#how-it-works">How it works</a>
            <a className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground" href="#pricing">Pricing</a>
          </nav>

          <div className="flex items-center gap-3">
            <Button asChild className="hidden sm:inline-flex" size="sm">
              <a href="#pricing">Explore plans <ArrowRight aria-hidden="true" /></a>
            </Button>
            <Button
              aria-expanded={menuOpen}
              aria-label={menuOpen ? "Close navigation menu" : "Open navigation menu"}
              className="md:hidden"
              onClick={() => setMenuOpen((open) => !open)}
              size="icon"
              variant="ghost"
            >
              {menuOpen ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
            </Button>
          </div>
        </div>
        {menuOpen && (
          <nav aria-label="Mobile navigation" className="border-t border-border px-5 py-3 md:hidden">
            {[
              ["Product", "#product"],
              ["Features", "#features"],
              ["How it works", "#how-it-works"],
              ["Pricing", "#pricing"],
            ].map(([label, href]) => (
              <a
                className="block py-3 text-sm font-medium text-foreground"
                href={href}
                key={href}
                onClick={closeMenu}
              >
                {label}
              </a>
            ))}
            <Button asChild className="mt-2 w-full">
              <a href="#pricing" onClick={closeMenu}>Explore plans <ArrowRight aria-hidden="true" /></a>
            </Button>
          </nav>
        )}
      </header>

      <section className="pilot-hero" id="top">
        <div className="mx-auto max-w-7xl px-5 pb-0 pt-16 sm:px-8 sm:pt-20 lg:pt-24">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1.5 text-xs font-semibold text-muted-foreground">
              <span className="size-2 rounded-full bg-pilot-teal" />
              A calmer way to support your customers
            </div>
            <h1 className="font-display text-5xl font-bold leading-[1.07] tracking-normal text-foreground sm:text-6xl lg:text-[72px]">
              Great support starts with <span className="text-primary">one clear view.</span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg sm:leading-8">
              Bring every customer conversation, teammate, and next step together—so your team can focus on thoughtful help, not tab overload.
            </p>
            <div className="mt-8 flex flex-col items-stretch justify-center gap-3 sm:flex-row sm:items-center">
              <Button asChild size="lg">
                <a href="#product">Meet your new support workspace <ArrowRight aria-hidden="true" /></a>
              </Button>
              <Button asChild size="lg" variant="outline">
                <a href="#how-it-works">See how it works</a>
              </Button>
            </div>
            <p className="mt-5 text-xs text-muted-foreground">Made for growing teams who care about every reply.</p>
          </div>

          <SupportWorkspace />

          <div className="mx-auto flex max-w-3xl flex-wrap items-center justify-center gap-x-7 gap-y-3 border-b border-border/80 py-7 text-xs font-medium text-muted-foreground sm:text-sm">
            <span className="inline-flex items-center gap-2"><Check aria-hidden="true" className="size-4 text-pilot-teal-deep" />Every conversation in one place</span>
            <span className="inline-flex items-center gap-2"><Check aria-hidden="true" className="size-4 text-pilot-teal-deep" />Clear ownership for every request</span>
            <span className="inline-flex items-center gap-2"><Check aria-hidden="true" className="size-4 text-pilot-teal-deep" />Built around your team</span>
          </div>
        </div>
      </section>

      <section className="pilot-section" id="product">
        <div className="mx-auto grid max-w-7xl gap-12 px-5 py-20 sm:px-8 sm:py-28 lg:grid-cols-[0.95fr_1.05fr] lg:items-center lg:gap-20">
          <div className="max-w-xl">
            <p className="pilot-kicker">A better way to work together</p>
            <h2 className="pilot-heading mt-4">Support feels different when the whole team is in sync.</h2>
            <p className="mt-5 text-base leading-7 text-muted-foreground">
              SupportPilot gives your team a shared home for customer conversations and the context behind them. Know what needs attention, who is on it, and what comes next.
            </p>
            <a className="mt-7 inline-flex items-center gap-2 text-sm font-semibold text-primary transition-colors hover:text-pilot-blue" href="#features">
              Get to know the workspace <ArrowRight aria-hidden="true" className="size-4" />
            </a>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:gap-4">
            <div className="pilot-stat-panel col-span-2 flex min-h-36 items-center justify-between gap-5 p-6 sm:p-8">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Your team’s support picture</p>
                <p className="mt-2 font-display text-3xl font-bold sm:text-4xl">All in one place.</p>
              </div>
              <span className="flex size-12 shrink-0 items-center justify-center rounded-lg bg-pilot-teal-soft text-pilot-teal-deep">
                <Layers3 aria-hidden="true" className="size-6" />
              </span>
            </div>
            <div className="pilot-stat-panel min-h-40 p-5 sm:p-6">
              <span className="flex size-10 items-center justify-center rounded-lg bg-pilot-blue-soft text-pilot-blue"><UsersRound aria-hidden="true" className="size-5" /></span>
              <p className="mt-5 text-sm font-semibold">Shared team context</p>
              <p className="mt-1 text-xs leading-5 text-muted-foreground">Pass conversations along without losing the details.</p>
            </div>
            <div className="pilot-stat-panel min-h-40 p-5 sm:p-6">
              <span className="flex size-10 items-center justify-center rounded-lg bg-pilot-coral-soft text-pilot-coral"><Activity aria-hidden="true" className="size-5" /></span>
              <p className="mt-5 text-sm font-semibold">A clearer picture</p>
              <p className="mt-1 text-xs leading-5 text-muted-foreground">See patterns and make the next improvement count.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="pilot-tinted-section" id="features">
        <div className="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-28">
          <div className="mx-auto max-w-2xl text-center">
            <p className="pilot-kicker">Thoughtfully connected</p>
            <h2 className="pilot-heading mt-4">Everything your support team needs to move forward.</h2>
            <p className="mt-4 text-base leading-7 text-muted-foreground">Less jumping between tools. More time for the people who need you.</p>
          </div>
          <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <FeatureCard icon={<Inbox aria-hidden="true" />} tone="blue" title="One shared inbox">
              Bring requests into one organized view and keep every conversation easy to find.
            </FeatureCard>
            <FeatureCard icon={<Workflow aria-hidden="true" />} tone="teal" title="Thoughtful routing">
              Make ownership clear and help each request reach the right teammate.
            </FeatureCard>
            <FeatureCard icon={<MessageSquareText aria-hidden="true" />} tone="coral" title="Useful context">
              Keep the customer story close, so every reply feels personal and informed.
            </FeatureCard>
            <FeatureCard icon={<BarChart3 aria-hidden="true" />} tone="gold" title="Team insights">
              Spot recurring questions and understand where your support can improve.
            </FeatureCard>
          </div>
        </div>
      </section>

      <section className="pilot-section" id="how-it-works">
        <div className="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-28">
          <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
            <div className="max-w-2xl">
              <p className="pilot-kicker">Up and running, together</p>
              <h2 className="pilot-heading mt-4">A smoother support rhythm in three steps.</h2>
            </div>
            <p className="max-w-sm text-sm leading-6 text-muted-foreground">Start with the conversations you already have. Build a better way of working around them.</p>
          </div>
          <div className="mt-12 grid gap-8 md:grid-cols-3 md:gap-10">
            <StepCard number="01" icon={<Layers3 aria-hidden="true" />} title="Bring conversations together">
              Connect your support channels and give your team one place to see what’s happening.
            </StepCard>
            <StepCard number="02" icon={<UsersRound aria-hidden="true" />} title="Make ownership clear">
              Share context, route requests, and keep the next step visible to everyone.
            </StepCard>
            <StepCard number="03" icon={<BarChart3 aria-hidden="true" />} title="Keep getting better">
              Learn from the questions customers ask and make each handoff more thoughtful.
            </StepCard>
          </div>
        </div>
      </section>

      <section className="pilot-tinted-section" id="pricing">
        <div className="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-28">
          <div className="mx-auto max-w-2xl text-center">
            <p className="pilot-kicker">Flexible by design</p>
            <h2 className="pilot-heading mt-4">The right setup for the way your team works.</h2>
            <p className="mt-4 text-base leading-7 text-muted-foreground">
              Choose a starting point, then tailor the details to your team size and support needs. Pricing is available by conversation.
            </p>
          </div>
          <div className="mx-auto mt-12 grid max-w-6xl gap-4 lg:grid-cols-3">
            <PlanCard
              description="A focused home for a small, hands-on support team."
              features={["Shared support inbox", "Team assignment and handoffs", "Customer conversation history"]}
              name="Essentials"
            />
            <PlanCard
              description="More structure for a growing team and a busier inbox."
              featured
              features={["Everything in Essentials", "Flexible routing workflows", "Team and conversation insights"]}
              name="Growth"
            />
            <PlanCard
              description="A tailored setup for complex, multi-team support."
              features={["Everything in Growth", "Multi-team workspace planning", "Guided setup for your support operation"]}
              name="Enterprise"
            />
          </div>
          <p className="mt-6 text-center text-xs text-muted-foreground">Every team’s needs are different. Talk with us about a plan that fits.</p>
        </div>
      </section>

      <footer className="border-t border-border bg-background" id="contact">
        <div className="mx-auto flex max-w-7xl flex-col gap-8 px-5 py-10 sm:px-8 md:flex-row md:items-center md:justify-between">
          <a className="flex items-center gap-3" href="#top" aria-label="SupportPilot home">
            <span className="flex size-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <LifeBuoy aria-hidden="true" className="size-[18px]" />
            </span>
            <span className="font-display text-lg font-bold">SupportPilot</span>
          </a>
          <nav aria-label="Footer navigation" className="flex flex-wrap gap-x-6 gap-y-3 text-sm text-muted-foreground">
            <a className="transition-colors hover:text-foreground" href="#product">Product</a>
            <a className="transition-colors hover:text-foreground" href="#features">Features</a>
            <a className="transition-colors hover:text-foreground" href="#how-it-works">How it works</a>
            <a className="transition-colors hover:text-foreground" href="#pricing">Pricing</a>
          </nav>
          <p className="text-xs text-muted-foreground">Thoughtful support starts here.</p>
        </div>
      </footer>
    </main>
  );
}

function SupportWorkspace() {
  return (
    <div aria-label="Illustration of the SupportPilot customer support workspace" className="pilot-workspace mx-auto mt-14 max-w-6xl sm:mt-16" role="img">
      <div className="flex h-12 items-center justify-between border-b border-border bg-card px-3 sm:px-5">
        <div className="flex items-center gap-2.5">
          <span className="flex size-7 items-center justify-center rounded-md bg-primary text-primary-foreground"><LifeBuoy aria-hidden="true" className="size-4" /></span>
          <span className="hidden text-xs font-semibold sm:inline">SupportPilot</span>
          <span className="mx-1 hidden h-4 border-l border-border sm:block" />
          <span className="flex items-center gap-1.5 text-[11px] font-medium text-muted-foreground sm:text-xs">Northstar Studio <ChevronDown aria-hidden="true" className="size-3" /></span>
        </div>
        <div className="flex items-center gap-2.5 text-muted-foreground sm:gap-4">
          <span className="hidden items-center gap-1.5 rounded-md border border-border px-2 py-1 text-[10px] sm:inline-flex"><Search aria-hidden="true" className="size-3" /> Search <span className="rounded bg-muted px-1">⌘ K</span></span>
          <CircleHelp aria-hidden="true" className="size-4" />
          <span className="flex size-7 items-center justify-center rounded-full bg-pilot-coral-soft text-[10px] font-bold text-pilot-coral">AM</span>
        </div>
      </div>

      <div className="grid min-h-[390px] grid-cols-[48px_minmax(0,1fr)] lg:grid-cols-[175px_minmax(0,1fr)_222px]">
        <aside aria-hidden="true" className="border-r border-border bg-muted/40 p-2.5 sm:p-4 lg:p-4">
          <div className="mb-5 hidden items-center justify-between text-[10px] font-semibold uppercase tracking-normal text-muted-foreground lg:flex">Workspace <MoreHorizontal aria-hidden="true" className="size-4" /></div>
          <div className="space-y-2">
            <WorkspaceNavItem active icon={<Inbox aria-hidden="true" />} label="Inbox" count="12" />
            <WorkspaceNavItem icon={<Layers3 aria-hidden="true" />} label="Views" />
            <WorkspaceNavItem icon={<UsersRound aria-hidden="true" />} label="Customers" />
            <WorkspaceNavItem icon={<BarChart3 aria-hidden="true" />} label="Insights" />
          </div>
          <div className="mb-2 mt-7 hidden text-[10px] font-semibold uppercase tracking-normal text-muted-foreground lg:block">Your team</div>
          <div className="hidden space-y-2.5 lg:block">
            <p className="flex items-center gap-2 text-[11px] text-muted-foreground"><span className="size-2 rounded-full bg-pilot-teal" /> Maya Chen <span className="ml-auto">4</span></p>
            <p className="flex items-center gap-2 text-[11px] text-muted-foreground"><span className="size-2 rounded-full bg-pilot-coral" /> Alex Morgan <span className="ml-auto">3</span></p>
            <p className="flex items-center gap-2 text-[11px] text-muted-foreground"><span className="size-2 rounded-full bg-pilot-blue" /> Sam Rivera <span className="ml-auto">5</span></p>
          </div>
          <div className="mt-8 hidden border-t border-border pt-4 text-[11px] text-muted-foreground lg:block">Help center <ArrowUpRight aria-hidden="true" className="ml-1 inline size-3" /></div>
        </aside>

        <div className="min-w-0 bg-card">
          <div className="flex h-12 items-center justify-between border-b border-border px-3 sm:px-5">
            <div className="flex items-center gap-2.5"><h3 className="text-sm font-semibold">Inbox</h3><span className="rounded-full bg-pilot-blue-soft px-2 py-0.5 text-[10px] font-semibold text-pilot-blue">12 open</span></div>
            <div className="flex items-center gap-2 text-muted-foreground"><Search aria-hidden="true" className="size-4" /><MoreHorizontal aria-hidden="true" className="size-4" /></div>
          </div>
          <div className="grid h-[338px] grid-cols-[minmax(105px,0.82fr)_minmax(0,1.45fr)] sm:grid-cols-[minmax(165px,0.82fr)_minmax(0,1.45fr)]">
            <div className="overflow-hidden border-r border-border">
              <div className="flex items-center justify-between border-b border-border px-2.5 py-3 sm:px-3"><span className="text-[10px] font-semibold sm:text-[11px]">All conversations</span><span className="text-[10px] text-muted-foreground">Filter</span></div>
              <ConversationItem active initials="JL" name="Jordan Lee" subject="A question about my order" time="2m" color="blue">Hi there, I was wondering if you could help me track…</ConversationItem>
              <ConversationItem initials="SK" name="Sofia Kim" subject="Updating my details" time="18m" color="teal">I moved recently and need to update the address…</ConversationItem>
              <ConversationItem initials="MT" name="Morgan Taylor" subject="Thank you for your help" time="1h" color="coral">That cleared everything up. Appreciate it!</ConversationItem>
              <ConversationItem initials="DP" name="Dev Patel" subject="Invoice for this month" time="3h" color="gold">Could you send a copy of the invoice to our team?</ConversationItem>
            </div>
            <div className="relative flex min-w-0 flex-col">
              <div className="flex items-center justify-between gap-1 border-b border-border px-3 py-3 sm:px-5">
                <div className="min-w-0"><div className="flex items-center gap-1.5"><p className="truncate text-xs font-semibold sm:text-sm">A question about my order</p><span className="hidden rounded bg-pilot-coral-soft px-1.5 py-0.5 text-[9px] font-medium text-pilot-coral sm:inline-flex">Needs reply</span></div><p className="mt-1 text-[10px] text-muted-foreground">Jordan Lee · via email</p></div>
                <span className="flex size-7 shrink-0 items-center justify-center rounded-md border border-border text-muted-foreground"><MoreHorizontal aria-hidden="true" className="size-4" /></span>
              </div>
              <div className="flex-1 space-y-4 overflow-hidden px-3 py-4 sm:px-5">
                <p className="text-center text-[9px] text-muted-foreground">Today, 10:42 AM</p>
                <div className="flex items-start gap-2">
                  <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-pilot-blue-soft text-[9px] font-semibold text-pilot-blue">JL</span>
                  <div className="max-w-[92%] rounded-r-lg rounded-bl-lg border border-border bg-background px-3 py-2.5">
                    <p className="text-[10px] font-semibold">Jordan Lee <span className="ml-1 font-normal text-muted-foreground">10:42 AM</span></p>
                    <p className="mt-1 text-[10px] leading-4 text-muted-foreground sm:text-[11px] sm:leading-5">Hi there! I’m trying to find the delivery update for my recent order. Could you point me in the right direction?</p>
                  </div>
                </div>
                <div className="flex items-start justify-end gap-2">
                  <div className="max-w-[90%] rounded-l-lg rounded-br-lg bg-pilot-blue-soft px-3 py-2.5">
                    <p className="text-[10px] font-semibold">Maya Chen <span className="ml-1 font-normal text-muted-foreground">10:48 AM</span></p>
                    <p className="mt-1 text-[10px] leading-4 text-muted-foreground sm:text-[11px] sm:leading-5">Of course, Jordan. I’m checking the latest details for you now and will be right back with an update.</p>
                  </div>
                  <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-pilot-teal-soft text-[9px] font-semibold text-pilot-teal-deep">MC</span>
                </div>
                <div className="flex items-center gap-1.5 text-[9px] text-muted-foreground"><Clock3 aria-hidden="true" className="size-3" /> Maya is working on this conversation</div>
              </div>
              <div className="mx-3 mb-3 rounded-md border border-border p-2.5 sm:mx-5 sm:mb-4 sm:p-3">
                <p className="text-[10px] text-muted-foreground">Reply to Jordan…</p>
                <div className="mt-4 flex items-center justify-between"><span className="flex items-center gap-2 text-muted-foreground"><span className="font-serif text-sm font-bold">B</span><span className="text-xs italic">I</span><span className="text-xs">↗</span></span><span className="flex size-6 items-center justify-center rounded bg-primary text-primary-foreground"><Send aria-hidden="true" className="size-3" /></span></div>
              </div>
            </div>
          </div>
        </div>

        <aside aria-hidden="true" className="hidden border-l border-border bg-muted/30 p-4 lg:block">
          <div className="flex items-center justify-between"><p className="text-[11px] font-semibold">Conversation details</p><MoreHorizontal aria-hidden="true" className="size-4 text-muted-foreground" /></div>
          <div className="mt-5 flex items-center gap-2.5"><span className="flex size-9 items-center justify-center rounded-full bg-pilot-blue-soft text-xs font-semibold text-pilot-blue">JL</span><div><p className="text-[11px] font-semibold">Jordan Lee</p><p className="text-[9px] text-muted-foreground">jordan@example.com</p></div></div>
          <div className="mt-5 space-y-3 border-y border-border py-4 text-[10px]"><p className="flex justify-between text-muted-foreground">Status <span className="font-medium text-foreground">Open</span></p><p className="flex justify-between text-muted-foreground">Assigned to <span className="font-medium text-foreground">Maya Chen</span></p><p className="flex justify-between text-muted-foreground">Channel <span className="font-medium text-foreground">Email</span></p></div>
          <div className="mt-5"><p className="text-[10px] font-semibold">Customer history</p><div className="mt-3 rounded-md border border-border bg-card p-2.5"><p className="text-[9px] font-medium">Previous conversation</p><p className="mt-1 text-[9px] leading-4 text-muted-foreground">Question about a recent purchase</p><p className="mt-2 text-[9px] text-muted-foreground">Last week</p></div></div>
          <div className="mt-4 rounded-md border border-pilot-teal/20 bg-pilot-teal-soft/50 p-2.5"><p className="flex items-center gap-1.5 text-[9px] font-semibold text-pilot-teal-deep"><ShieldCheck aria-hidden="true" className="size-3" /> Shared with your team</p><p className="mt-1 text-[9px] leading-4 text-muted-foreground">Recent context is ready for the next teammate.</p></div>
        </aside>
      </div>
      <div className="flex items-center justify-between border-t border-border bg-card px-3 py-2 sm:px-5">
        <span className="flex items-center gap-1.5 text-[9px] text-muted-foreground"><span className="size-1.5 rounded-full bg-pilot-teal" />Your team workspace</span>
        <span className="flex items-center gap-1.5 text-[9px] text-muted-foreground">Updated just now <Zap aria-hidden="true" className="size-3" /></span>
      </div>
    </div>
  );
}

function WorkspaceNavItem({
  active = false,
  count,
  icon,
  label,
}: {
  active?: boolean;
  count?: string;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <div className={`flex items-center justify-center gap-2 rounded-md px-2 py-2 lg:justify-start ${active ? "bg-pilot-blue-soft text-pilot-blue" : "text-muted-foreground"}`}>
      <span className="shrink-0">{icon}</span>
      <span className="hidden text-[11px] font-medium lg:inline">{label}</span>
      {count && <span className="hidden text-[10px] lg:ml-auto lg:inline">{count}</span>}
    </div>
  );
}

function ConversationItem({
  active = false,
  children,
  color,
  initials,
  name,
  subject,
  time,
}: {
  active?: boolean;
  children: React.ReactNode;
  color: "blue" | "teal" | "coral" | "gold";
  initials: string;
  name: string;
  subject: string;
  time: string;
}) {
  const avatarTone = {
    blue: "bg-pilot-blue-soft text-pilot-blue",
    teal: "bg-pilot-teal-soft text-pilot-teal-deep",
    coral: "bg-pilot-coral-soft text-pilot-coral",
    gold: "bg-pilot-gold-soft text-pilot-gold-deep",
  }[color];

  return (
    <div className={`border-b border-border px-2.5 py-3 sm:px-3 ${active ? "bg-pilot-blue-soft/60" : "bg-card"}`}>
      <div className="flex items-center gap-2">
        <span className={`flex size-6 shrink-0 items-center justify-center rounded-full text-[8px] font-bold ${avatarTone}`}>{initials}</span>
        <span className="min-w-0 truncate text-[9px] font-semibold sm:text-[10px]">{name}</span>
        <span className="ml-auto shrink-0 text-[8px] text-muted-foreground">{time}</span>
      </div>
      <p className="mt-2 truncate text-[9px] font-medium">{subject}</p>
      <p className="mt-1 truncate text-[8px] leading-4 text-muted-foreground">{children}</p>
    </div>
  );
}

function FeatureCard({
  children,
  icon,
  title,
  tone,
}: {
  children: React.ReactNode;
  icon: React.ReactNode;
  title: string;
  tone: "blue" | "teal" | "coral" | "gold";
}) {
  const iconTone = {
    blue: "bg-pilot-blue-soft text-pilot-blue",
    teal: "bg-pilot-teal-soft text-pilot-teal-deep",
    coral: "bg-pilot-coral-soft text-pilot-coral",
    gold: "bg-pilot-gold-soft text-pilot-gold-deep",
  }[tone];

  return (
    <article className="pilot-feature-item">
      <span className={`flex size-11 items-center justify-center rounded-lg [&_svg]:size-5 ${iconTone}`}>{icon}</span>
      <h3 className="mt-6 text-base font-semibold">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-muted-foreground">{children}</p>
    </article>
  );
}

function StepCard({
  children,
  icon,
  number,
  title,
}: {
  children: React.ReactNode;
  icon: React.ReactNode;
  number: string;
  title: string;
}) {
  return (
    <article className="relative border-t border-border pt-6">
      <div className="flex items-center justify-between">
        <span className="flex size-10 items-center justify-center rounded-lg bg-pilot-blue-soft text-pilot-blue [&_svg]:size-5">{icon}</span>
        <span className="font-display text-sm font-semibold text-muted-foreground">{number}</span>
      </div>
      <h3 className="mt-6 text-lg font-semibold">{title}</h3>
      <p className="mt-2 max-w-sm text-sm leading-6 text-muted-foreground">{children}</p>
    </article>
  );
}

function PlanCard({
  description,
  featured = false,
  features,
  name,
}: {
  description: string;
  featured?: boolean;
  features: string[];
  name: string;
}) {
  return (
    <article className={`pilot-plan ${featured ? "pilot-plan-featured" : ""}`}>
      <div className="flex min-h-7 items-center justify-between gap-2">
        <p className="text-sm font-semibold">{name}</p>
        {featured && <span className="rounded-full bg-pilot-teal-soft px-2.5 py-1 text-[10px] font-semibold text-pilot-teal-deep">Most popular</span>}
      </div>
      <p className="mt-3 font-display text-3xl font-bold">Custom</p>
      <p className="mt-1 text-xs text-muted-foreground">Tailored to your team</p>
      <p className="mt-5 min-h-12 text-sm leading-6 text-muted-foreground">{description}</p>
      <Button asChild className="mt-6 w-full" variant={featured ? "default" : "outline"}>
        <a href="#features">Explore features <ArrowRight aria-hidden="true" /></a>
      </Button>
      <div className="mt-6 border-t border-border pt-5">
        <p className="mb-4 text-xs font-semibold">A place to start</p>
        <ul className="space-y-3">
          {features.map((feature) => (
            <li className="flex items-start gap-2.5 text-xs leading-5 text-muted-foreground" key={feature}>
              <Check aria-hidden="true" className="mt-0.5 size-3.5 shrink-0 text-pilot-teal-deep" />
              <span>{feature}</span>
            </li>
          ))}
        </ul>
      </div>
    </article>
  );
}
