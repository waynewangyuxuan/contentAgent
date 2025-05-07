import type React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Wrench, Search, Globe, Twitter, Send } from "lucide-react"

interface ToolsPanelProps {
  tools: {
    [key: string]: string
  }
}

export function ToolsPanel({ tools }: ToolsPanelProps) {
  // Map tool names to icons
  const toolIcons: { [key: string]: React.ReactNode } = {
    search: <Search className="h-4 w-4" />,
    fetch_content: <Globe className="h-4 w-4" />,
    generate_tweet: <Twitter className="h-4 w-4" />,
    post_tweet: <Send className="h-4 w-4" />,
  }

  return (
    <Card className="bg-white/80 backdrop-blur-sm border-emerald-100">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg flex items-center gap-2 text-emerald-800">
          <Wrench className="h-5 w-5" />
          Available Tools
        </CardTitle>
      </CardHeader>
      <CardContent>
        {Object.keys(tools).length === 0 ? (
          <div className="text-center py-4 text-emerald-700/70">
            <p>No tools available</p>
          </div>
        ) : (
          <ul className="space-y-3">
            {Object.entries(tools).map(([name, description]) => (
              <li key={name} className="flex items-start gap-2 pb-2 border-b border-emerald-50 last:border-0">
                <div className="bg-emerald-100 p-1.5 rounded-md text-emerald-700 mt-0.5">
                  {toolIcons[name] || <Wrench className="h-4 w-4" />}
                </div>
                <div>
                  <p className="text-sm font-medium text-emerald-800">{name.replace(/_/g, " ")}</p>
                  <p className="text-xs text-emerald-600">{description}</p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}
