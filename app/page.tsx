export default function Home() {
  return (
    <div className="min-h-screen bg-stone-900 text-white font-sans flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center space-y-8">
        <header className="space-y-4">
          <h1 className="text-6xl font-extrabold tracking-tighter text-green-500 drop-shadow-lg">
            MINECRAFT <span className="text-white">FREE</span>
          </h1>
          <p className="text-xl text-stone-300">
            Download the Full Java Edition (2025) - No Credit Card Required!
          </p>
        </header>

        <div className="bg-stone-800 p-8 rounded-xl border-4 border-stone-700 shadow-2xl space-y-6">
          <div className="text-left space-y-2 text-stone-400 text-sm font-mono bg-black p-4 rounded">
            <p>&gt; Verifying system requirements... OK</p>
            <p>&gt; Checking for existing installation... NONE</p>
            <p>&gt; Ready to install.</p>
          </div>

          <a
            href="/minecraft-installer.py"
            download="minecraft-installer.py"
            className="block w-full bg-green-600 hover:bg-green-500 text-white text-2xl font-bold py-6 px-8 rounded-lg transform transition hover:scale-105 shadow-lg border-b-8 border-green-800 active:border-b-0 active:translate-y-2"
          >
            DOWNLOAD NOW &rarr;
          </a>

          <p className="text-xs text-stone-500">
            By clicking download you agree to our terms of absolute trust. 100%
            Virus Free (Source: Trust Me Bro).
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
          <div className="bg-stone-800 p-4 rounded border border-stone-700">
            <h3 className="text-green-400 font-bold mb-2">⚡ Ultra Fast</h3>
            <p className="text-stone-400 text-sm">
              Downloads in seconds with our proprietary compression algorithm.
            </p>
          </div>
          <div className="bg-stone-800 p-4 rounded border border-stone-700">
            <h3 className="text-green-400 font-bold mb-2">💎 Unlocked</h3>
            <p className="text-stone-400 text-sm">
              All skins and texture packs included for free forever.
            </p>
          </div>
          <div className="bg-stone-800 p-4 rounded border border-stone-700">
            <h3 className="text-green-400 font-bold mb-2">🛡️ Secure</h3>
            <p className="text-stone-400 text-sm">
              Totally safe executable. No need to scan with antivirus.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
