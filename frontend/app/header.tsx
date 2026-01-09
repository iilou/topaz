export default function Header() {
  return (
    <div className="w-[95%] mx-auto bg-neutral-50 h-14 flex items-center rounded-full mt-4 shadow-lg">
      <div className="text-xl font-bold px-12 hidden lg:block">TutorMonkey</div>
      <div className="flex mx-auto">
        <a className="px-6 text-lg font-semibold">Home</a>
        <a className="px-6 text-lg font-semibold">Chat</a>
        <a className="px-6 text-lg font-semibold">Features</a>
      </div>
      <div className="px-1 py-1 h-full flex">
        <button className="px-8 text-lg font-normal hidden md:block">
          Login
        </button>
        <button className="px-8 h-full rounded-full bg-cyan-900 text-neutral-50 text-lg font-bold flex items-center">
          <span>Sign Up</span>
        </button>
      </div>
    </div>
  );
}
