"use client"

import { useState, useEffect, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"
import { Keyboard, Volume2, Headphones, Play, Pause, Music, Settings, VolumeX, Volume1, Zap, Info } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

const soundProfiles = [
  { name: "blue", description: "Cherry MX Blue style - Sharp, clicky", category: "Classic", file: "keyboard_blue.wav" },
  {
    name: "brown",
    description: "Cherry MX Brown style - Tactile bump",
    category: "Classic",
    file: "keyboard_brown.wav",
  },
  { name: "red", description: "Cherry MX Red style - Linear, quiet", category: "Classic", file: "keyboard_red.wav" },
  {
    name: "mechanical",
    description: "Heavy mechanical - Loud, satisfying",
    category: "Mechanical",
    file: "keyboard_mechanical.wav",
  },
  {
    name: "creamy",
    description: "Lubed switches - Smooth, premium",
    category: "Mechanical",
    file: "keyboard_creamy.wav",
  },
  { name: "dry", description: "Unlubricated - Scratchy, raw", category: "Mechanical", file: "keyboard_dry.wav" },
  { name: "thock", description: "Topre-style - Deep, muffled", category: "Mechanical", file: "keyboard_thock.wav" },
  { name: "clicky", description: "Box Jade/Navy - Extra clicky", category: "Mechanical", file: "keyboard_clicky.wav" },
  {
    name: "silent",
    description: "Dampened switches - Quiet, subtle",
    category: "Mechanical",
    file: "keyboard_silent.wav",
  },
  {
    name: "tactile",
    description: "Pronounced bump - Sharp tactile",
    category: "Mechanical",
    file: "keyboard_tactile.wav",
  },
  {
    name: "hard",
    description: "Extremely aggressive - Metal-on-metal violence",
    category: "Mechanical",
    file: "keyboard_hard.wav",
  },
  {
    name: "typewriter",
    description: "Vintage typewriter - Metallic, classic",
    category: "Vintage",
    file: "keyboard_typewriter.wav",
  },
  { name: "lofi", description: "Chill, warm - Nostalgic, soft", category: "Vintage", file: "keyboard_lofi.wav" },
  {
    name: "gx_feryn",
    description: "Gaming optimized - Smooth, precise",
    category: "Special",
    file: "keyboard_gx_feryn.wav",
  },
  {
    name: "lee_sin",
    description: "Martial arts inspired - Sharp, precise strikes",
    category: "Special",
    file: "keyboard_lee_sin.wav",
  },
  {
    name: "hacker",
    description: "Retro terminal - Matrix-like, digital",
    category: "Special",
    file: "keyboard_hacker.wav",
  },
]

const features = [
  {
    icon: <Headphones className="h-6 w-6" />,
    title: "Real-time Audio",
    description: "Instant keyboard sound feedback with Web Audio API",
  },
  {
    icon: <Zap className="h-6 w-6" />,
    title: "Browser Hotkeys",
    description: "Space to toggle, Arrow keys to switch sounds",
  },
  {
    icon: <Music className="h-6 w-6" />,
    title: "16 Sound Profiles",
    description: "From classic Cherry MX to aggressive mechanical sounds",
  },
  {
    icon: <Settings className="h-6 w-6" />,
    title: "Volume Control",
    description: "Adjustable volume with visual feedback",
  },
]

export default function Home() {
  const [currentSound, setCurrentSound] = useState("blue")
  const [isEnabled, setIsEnabled] = useState(false)
  const [volume, setVolume] = useState([0.5])
  const [audioContext, setAudioContext] = useState<AudioContext | null>(null)
  const [audioBuffers, setAudioBuffers] = useState<Map<string, AudioBuffer>>(new Map())
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  // Initialize audio context
  useEffect(() => {
    const initAudio = async () => {
      try {
        const ctx = new (window.AudioContext || (window as any).webkitAudioContext)()
        setAudioContext(ctx)

        // Load all sound files
        setIsLoading(true)
        const buffers = new Map<string, AudioBuffer>()

        for (const profile of soundProfiles) {
          try {
            const response = await fetch(`/generated_sounds/${profile.file}`)
            if (response.ok) {
              const arrayBuffer = await response.arrayBuffer()
              const audioBuffer = await ctx.decodeAudioData(arrayBuffer)
              buffers.set(profile.name, audioBuffer)
            }
          } catch (error) {
            console.log(`[v0] Failed to load ${profile.file}:`, error)
          }
        }

        setAudioBuffers(buffers)
        setIsLoading(false)

        if (buffers.size > 0) {
          toast({
            title: "Audio System Ready",
            description: `Loaded ${buffers.size} sound profiles`,
          })
        } else {
          toast({
            title: "Audio Warning",
            description: "No sound files found - using silent mode",
            variant: "destructive",
          })
        }
      } catch (error) {
        console.log("[v0] Audio initialization failed:", error)
        setIsLoading(false)
        toast({
          title: "Audio Error",
          description: "Failed to initialize audio system",
          variant: "destructive",
        })
      }
    }

    initAudio()
  }, [toast])

  // Play sound function
  const playSound = useCallback(
    (soundName: string) => {
      if (!audioContext || !audioBuffers.has(soundName) || !isEnabled) return

      try {
        const buffer = audioBuffers.get(soundName)!
        const source = audioContext.createBufferSource()
        const gainNode = audioContext.createGain()

        source.buffer = buffer
        gainNode.gain.value = volume[0]

        source.connect(gainNode)
        gainNode.connect(audioContext.destination)

        source.start()
      } catch (error) {
        console.log("[v0] Sound playback error:", error)
      }
    },
    [audioContext, audioBuffers, isEnabled, volume],
  )

  // Keyboard event listener
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ignore if typing in input fields
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
        return
      }

      // Global hotkeys
      if (event.code === "Space" && !event.repeat) {
        event.preventDefault()
        setIsEnabled((prev) => !prev)
        return
      }

      if (event.code === "ArrowUp" && event.shiftKey) {
        event.preventDefault()
        const currentIndex = soundProfiles.findIndex((p) => p.name === currentSound)
        const nextIndex = (currentIndex + 1) % soundProfiles.length
        setCurrentSound(soundProfiles[nextIndex].name)
        return
      }

      if (event.code === "ArrowDown" && event.shiftKey) {
        event.preventDefault()
        const currentIndex = soundProfiles.findIndex((p) => p.name === currentSound)
        const prevIndex = (currentIndex - 1 + soundProfiles.length) % soundProfiles.length
        setCurrentSound(soundProfiles[prevIndex].name)
        return
      }

      // Play sound for regular typing
      if (!event.repeat && isEnabled) {
        playSound(currentSound)
      }
    }

    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [currentSound, isEnabled, playSound])

  const groupedSounds = soundProfiles.reduce(
    (acc, sound) => {
      if (!acc[sound.category]) acc[sound.category] = []
      acc[sound.category].push(sound)
      return acc
    },
    {} as Record<string, typeof soundProfiles>,
  )

  const switchSound = (soundName: string) => {
    setCurrentSound(soundName)
    toast({
      title: "Sound Changed",
      description: `Switched to ${soundName} sound`,
    })

    // Play preview
    if (isEnabled && audioBuffers.has(soundName)) {
      playSound(soundName)
    }
  }

  const testSound = () => {
    if (audioBuffers.has(currentSound)) {
      playSound(currentSound)
    } else {
      toast({
        title: "Sound Not Available",
        description: `${currentSound} sound file not loaded`,
        variant: "destructive",
      })
    }
  }

  const toggleEnabled = () => {
    setIsEnabled((prev) => {
      const newState = !prev
      toast({
        title: newState ? "Keyboard Sounds Enabled" : "Keyboard Sounds Disabled",
        description: newState ? "Start typing to hear sounds!" : "Keyboard sounds are now muted",
      })
      return newState
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Keyboard className="h-12 w-12 text-blue-600" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              enx-kebod
            </h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Transform any keyboard into a satisfying mechanical keyboard experience - now running in your browser!
          </p>
          <div className="flex items-center justify-center gap-4 mt-6">
            <Badge variant={isEnabled ? "default" : "secondary"} className="text-sm">
              {isEnabled ? <Volume2 className="h-4 w-4 mr-1" /> : <VolumeX className="h-4 w-4 mr-1" />}
              {isEnabled ? "Active" : "Disabled"}
            </Badge>
            <Badge variant="secondary" className="text-sm">
              <Music className="h-4 w-4 mr-1" />
              {currentSound}
            </Badge>
            <Badge variant="secondary" className="text-sm">
              <Zap className="h-4 w-4 mr-1" />
              Web Audio
            </Badge>
          </div>
        </div>

        {/* Quick Start Alert */}
        <Alert className="mb-8 border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-950">
          <Info className="h-4 w-4" />
          <AlertDescription className="text-sm">
            <strong>Quick Start:</strong> Press <code className="bg-blue-100 dark:bg-blue-900 px-1 rounded">Space</code>{" "}
            to toggle sounds, <code className="bg-blue-100 dark:bg-blue-900 px-1 rounded">Shift + ↑/↓</code> to switch
            profiles
          </AlertDescription>
        </Alert>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Control Panel */}
          <div className="lg:col-span-2">
            {/* Control Panel */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Control Panel
                </CardTitle>
                <CardDescription>
                  {isLoading ? "Loading sound profiles..." : "Control your keyboard sound experience"}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Enable/Disable Toggle */}
                <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                  <div className="flex items-center gap-3">
                    {isEnabled ? (
                      <Volume2 className="h-5 w-5 text-green-600" />
                    ) : (
                      <VolumeX className="h-5 w-5 text-gray-400" />
                    )}
                    <div>
                      <h3 className="font-medium">Keyboard Sounds</h3>
                      <p className="text-sm text-muted-foreground">
                        {isEnabled ? "Sounds will play when you type" : "Sounds are disabled"}
                      </p>
                    </div>
                  </div>
                  <Switch checked={isEnabled} onCheckedChange={toggleEnabled} disabled={isLoading} />
                </div>

                {/* Volume Control */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium">Volume</label>
                    <span className="text-sm text-muted-foreground">{Math.round(volume[0] * 100)}%</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Volume1 className="h-4 w-4 text-muted-foreground" />
                    <Slider value={volume} onValueChange={setVolume} max={1} step={0.1} className="flex-1" />
                    <Volume2 className="h-4 w-4 text-muted-foreground" />
                  </div>
                </div>

                {/* Test Sound */}
                <div className="flex items-center gap-3">
                  <Button onClick={testSound} disabled={isLoading} variant="outline" className="flex-1 bg-transparent">
                    <Play className="h-4 w-4 mr-2" />
                    Test Current Sound
                  </Button>
                  <Button onClick={toggleEnabled} disabled={isLoading} variant={isEnabled ? "destructive" : "default"}>
                    {isEnabled ? <Pause className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                    {isEnabled ? "Disable" : "Enable"}
                  </Button>
                </div>

                {/* Status Info */}
                <div className="text-sm text-muted-foreground bg-muted p-3 rounded-lg">
                  <div className="flex justify-between">
                    <span>Loaded sounds:</span>
                    <span>
                      {audioBuffers.size} / {soundProfiles.length}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Audio context:</span>
                    <span>{audioContext ? "Ready" : "Initializing..."}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Features */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Features</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  {features.map((feature, index) => (
                    <div key={index} className="flex gap-3 p-3 rounded-lg bg-muted">
                      <div className="text-blue-600 mt-1">{feature.icon}</div>
                      <div>
                        <h4 className="font-medium text-sm">{feature.title}</h4>
                        <p className="text-xs text-muted-foreground mt-1">{feature.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sound Profiles */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Music className="h-5 w-5" />
                  Sound Profiles
                </CardTitle>
                <CardDescription>16 different keyboard sounds to choose from</CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="Classic" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="Classic" className="text-xs">
                      Classic
                    </TabsTrigger>
                    <TabsTrigger value="Mechanical" className="text-xs">
                      Mechanical
                    </TabsTrigger>
                  </TabsList>
                  <TabsList className="grid w-full grid-cols-2 mt-2">
                    <TabsTrigger value="Vintage" className="text-xs">
                      Vintage
                    </TabsTrigger>
                    <TabsTrigger value="Special" className="text-xs">
                      Special
                    </TabsTrigger>
                  </TabsList>

                  {Object.entries(groupedSounds).map(([category, sounds]) => (
                    <TabsContent key={category} value={category} className="mt-4">
                      <div className="space-y-2">
                        {sounds.map((sound) => (
                          <div
                            key={sound.name}
                            className={`p-3 rounded-lg border cursor-pointer transition-colors hover:bg-muted ${
                              currentSound === sound.name
                                ? "border-blue-500 bg-blue-50 dark:bg-blue-950"
                                : "border-border"
                            }`}
                            onClick={() => switchSound(sound.name)}
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-medium text-sm">{sound.name}</span>
                              <div className="flex items-center gap-2">
                                {!audioBuffers.has(sound.name) && (
                                  <Badge variant="outline" className="text-xs">
                                    Missing
                                  </Badge>
                                )}
                                {sound.name === "hard" && (
                                  <Badge variant="destructive" className="text-xs">
                                    NEW
                                  </Badge>
                                )}
                              </div>
                            </div>
                            <p className="text-xs text-muted-foreground mt-1">{sound.description}</p>
                          </div>
                        ))}
                      </div>
                    </TabsContent>
                  ))}
                </Tabs>
              </CardContent>
            </Card>

            {/* Usage Instructions */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Keyboard className="h-5 w-5" />
                  How to Use
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <h4 className="font-medium text-sm">Keyboard Shortcuts</h4>
                  <div className="space-y-1 text-xs text-muted-foreground">
                    <div className="flex justify-between">
                      <span>Toggle sounds:</span>
                      <code className="bg-muted px-1 rounded">Space</code>
                    </div>
                    <div className="flex justify-between">
                      <span>Next profile:</span>
                      <code className="bg-muted px-1 rounded">Shift + ↑</code>
                    </div>
                    <div className="flex justify-between">
                      <span>Previous profile:</span>
                      <code className="bg-muted px-1 rounded">Shift + ↓</code>
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <h4 className="font-medium text-sm">Features</h4>
                  <ul className="text-xs text-muted-foreground space-y-1">
                    <li>• Real-time keyboard sound feedback</li>
                    <li>• 16 high-quality sound profiles</li>
                    <li>• Adjustable volume control</li>
                    <li>• Works entirely in your browser</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
