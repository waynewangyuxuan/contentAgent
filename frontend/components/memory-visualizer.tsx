import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Brain } from "lucide-react"

interface MemoryVisualizerProps {
  memoryStats?: {
    content_count: number
    facts_count: number
  }
  context: any
}

export function MemoryVisualizer({ memoryStats, context }: MemoryVisualizerProps) {
  const hasContext = context && Object.keys(context).length > 0

  return (
    <Card className="bg-white/80 backdrop-blur-sm border-emerald-100">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg flex items-center gap-2 text-emerald-800">
          <Brain className="h-5 w-5" />
          Memory & Context
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {!hasContext ? (
            <div className="text-center py-8 text-emerald-700/70 bg-emerald-50/50 rounded-lg">
              <p>No context available yet.</p>
              <p className="text-sm mt-2">Context will be built as you interact with the agent.</p>
            </div>
          ) : (
            <div>
              <p className="text-sm font-medium text-emerald-700 mb-2">Current Context:</p>
              <pre className="text-xs bg-emerald-50 p-3 rounded overflow-x-auto text-emerald-700 max-h-60">
                {JSON.stringify(context, null, 2)}
              </pre>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="relative overflow-hidden rounded-lg bg-gradient-to-br from-emerald-100 to-emerald-50 p-4 shadow-sm">
              <div className="relative z-10">
                <p className="text-2xl font-bold text-emerald-800">{memoryStats?.content_count || 0}</p>
                <p className="text-sm text-emerald-600">Content Items</p>
              </div>
              <div className="absolute bottom-0 right-0 opacity-10">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="text-emerald-800"
                  />
                </svg>
              </div>
            </div>

            <div className="relative overflow-hidden rounded-lg bg-gradient-to-br from-emerald-100 to-emerald-50 p-4 shadow-sm">
              <div className="relative z-10">
                <p className="text-2xl font-bold text-emerald-800">{memoryStats?.facts_count || 0}</p>
                <p className="text-sm text-emerald-600">Facts Stored</p>
              </div>
              <div className="absolute bottom-0 right-0 opacity-10">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="text-emerald-800"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
