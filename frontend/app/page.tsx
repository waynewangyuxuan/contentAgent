import { AgentDashboard } from "@/components/agent-dashboard"
import { GhibliBackground } from "@/components/ghibli-background"
import { ThemeProvider } from "@/components/theme-provider"

export default function Home() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="ghibli-agent-theme">
      <main className="min-h-screen relative overflow-hidden">
        <GhibliBackground />
        <div className="container relative z-10 mx-auto px-4 py-8">
          <AgentDashboard />
        </div>
      </main>
    </ThemeProvider>
  )
}
