import { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Adaptive LLaMA Proxy (ALP)',
  description: 'A proof-of-concept system demonstrating adaptive model compression for Llama 3.1',
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full bg-gray-50">
      <body className={`${inter.className} h-full`}>
        <div className="min-h-full">
          <nav className="bg-white shadow-sm">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="flex h-16 justify-between">
                <div className="flex">
                  <div className="flex flex-shrink-0 items-center">
                    <img className="h-8 w-auto" src="/logo.png" alt="ALP Logo" />
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <a href="#" className="inline-flex items-center border-b-2 border-indigo-500 px-1 pt-1 text-sm font-medium text-gray-900">
                      Dashboard
                    </a>
                    {/* Add more nav items as needed */}
                  </div>
                </div>
              </div>
            </div>
          </nav>

          <main>
            <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
              {children}
            </div>
          </main>

          <footer className="bg-white">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="border-t border-gray-200 py-4 text-center text-sm text-gray-500">
                © 2024 Adaptive LLaMA Proxy (ALP). All rights reserved.
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
