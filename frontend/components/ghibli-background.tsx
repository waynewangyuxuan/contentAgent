export function GhibliBackground() {
  return (
    <div className="fixed inset-0 z-0">
      <div className="absolute inset-0 bg-gradient-to-b from-emerald-50 to-teal-50/70"></div>

      {/* Decorative elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden opacity-10">
        <div className="absolute top-10 left-10 w-40 h-40 rounded-full bg-emerald-300 blur-3xl"></div>
        <div className="absolute bottom-10 right-10 w-60 h-60 rounded-full bg-teal-200 blur-3xl"></div>
        <div className="absolute top-1/3 right-1/4 w-40 h-40 rounded-full bg-emerald-100 blur-3xl"></div>
      </div>

      {/* Floating elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-[10%] w-8 h-8 bg-white rounded-full opacity-40 animate-float"></div>
        <div
          className="absolute top-40 right-[15%] w-6 h-6 bg-white rounded-full opacity-30 animate-float"
          style={{ animationDelay: "1s" }}
        ></div>
        <div
          className="absolute bottom-32 left-[20%] w-10 h-10 bg-white rounded-full opacity-50 animate-float"
          style={{ animationDelay: "2s" }}
        ></div>
        <div
          className="absolute bottom-40 right-[25%] w-5 h-5 bg-white rounded-full opacity-40 animate-float"
          style={{ animationDelay: "3s" }}
        ></div>
      </div>
    </div>
  )
}
