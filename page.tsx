'use client'
import { createClient } from '@supabase/supabase-js'
import { useState } from 'react'

// This uses the keys you put in .env.local
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export default function AuthPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('Welcome! Please Sign Up or Login.')

  const handleSignUp = async () => {
    const { error } = await supabase.auth.signUp({ email, password })
    if (error) setMessage("❌ Error: " + error.message)
    else setMessage('✅ Success! Check your email for a confirmation link.')
  }

  const handleLogin = async () => {
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) setMessage("❌ Error: " + error.message)
    else setMessage('✅ Success! You are securely logged in.')
  }

  return (
    <div style={{ 
      display: 'flex', flexDirection: 'column', alignItems: 'center', 
      justifyContent: 'center', height: '100vh', fontFamily: 'sans-serif',
      backgroundColor: '#f4f4f4' 
    }}>
      <div style={{ backgroundColor: 'white', padding: '40px', borderRadius: '10px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        <h1 style={{ marginBottom: '10px' }}>Secure Auth System</h1>
        <p style={{ color: '#666', marginBottom: '20px' }}>{message}</p>
        
        <input 
          type="email" placeholder="Email Address" 
          onChange={(e) => setEmail(e.target.value)} 
          style={{ display: 'block', width: '100%', marginBottom: '10px', padding: '12px', border: '1px solid #ccc', borderRadius: '5px' }}
        />
        <input 
          type="password" placeholder="Password" 
          onChange={(e) => setPassword(e.target.value)} 
          style={{ display: 'block', width: '100%', marginBottom: '20px', padding: '12px', border: '1px solid #ccc', borderRadius: '5px' }}
        />

        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={handleSignUp} style={{ flex: 1, padding: '10px', backgroundColor: '#0070f3', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
            Sign Up
          </button>
          <button onClick={handleLogin} style={{ flex: 1, padding: '10px', backgroundColor: '#10b981', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
            Login
          </button>
        </div>
      </div>
    </div>
  )
}