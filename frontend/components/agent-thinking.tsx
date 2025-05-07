import { Card, CardContent } from "@/components/ui/card"

export function AgentThinking() {
  return (
    <Card className="mt-8 bg-white/80 backdrop-blur-sm border-emerald-100">
      <CardContent className="pt-6">
        <div className="flex flex-col items-center justify-center py-8">
          <div className="relative w-24 h-24">
            {/* Animated thinking visualization */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-12 h-12 border-4 border-emerald-200 border-t-emerald-500 rounded-full animate-spin"></div>
            </div>
            <div className="absolute inset-0 flex items-center justify-center opacity-30">
              <div className="w-20 h-20 border-4 border-emerald-100 border-t-emerald-300 rounded-full animate-spin-slow"></div>
            </div>
            <div className="absolute inset-0 flex items-center justify-center opacity-20">
              <div className="w-16 h-16 border-4 border-emerald-50 border-b-emerald-200 rounded-full animate-reverse-spin"></div>
            </div>
          </div>

          <div className="mt-6 text-center">
            <h3 className="text-lg font-medium text-emerald-800">Thinking...</h3>
            <p className="text-sm text-emerald-600 mt-2 max-w-md">
              I'm analyzing your request and determining the best approach to help you.
            </p>
          </div>

          <div className="mt-4 flex space-x-2">
            <div className="h-2 w-2 bg-emerald-400 rounded-full animate-bounce"></div>
            <div
              className="h-2 w-2 bg-emerald-500 rounded-full animate-bounce"
              style={{ animationDelay: "0.2s" }}
            ></div>
            <div
              className="h-2 w-2 bg-emerald-600 rounded-full animate-bounce"
              style={{ animationDelay: "0.4s" }}
            ></div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
