import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { AgentStatus } from "@/components/agent-dashboard"
import { Activity, Server } from "lucide-react"

interface StatusPanelProps {
  status: AgentStatus | null
}

export function StatusPanel({ status }: StatusPanelProps) {
  return (
    <Card className="bg-white/80 backdrop-blur-sm border-emerald-100">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg flex items-center gap-2 text-emerald-800">
          <Server className="h-5 w-5" />
          Agent Status
        </CardTitle>
      </CardHeader>
      <CardContent>
        {!status ? (
          <div className="flex items-center justify-center h-24">
            <div className="h-6 w-6 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-emerald-600" />
              <span className="text-sm text-emerald-700">Status:</span>
              <Badge
                variant="outline"
                className={`ml-auto ${status.status === "running" ? "bg-green-100 text-green-800 hover:bg-green-100" : "bg-yellow-100 text-yellow-800 hover:bg-yellow-100"}`}
              >
                {status.status}
              </Badge>
            </div>

            <div className="grid grid-cols-2 gap-2 text-center">
              <div className="bg-emerald-50 p-2 rounded-lg">
                <div className="text-2xl font-semibold text-emerald-700">{status.memory_stats.content_count}</div>
                <div className="text-xs text-emerald-600">Content Items</div>
              </div>
              <div className="bg-emerald-50 p-2 rounded-lg">
                <div className="text-2xl font-semibold text-emerald-700">{status.memory_stats.facts_count}</div>
                <div className="text-xs text-emerald-600">Facts Stored</div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
