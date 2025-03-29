import { useState } from 'react'
import { 
  Container, 
  TextField, 
  Box, 
  Typography, 
  Paper,
  CircularProgress,
  Alert,
  Link
} from '@mui/material'
import { supabase } from './lib/supabase'

interface Character {
  id: number
  chapter: number
  serial: number
  character: string
  radical: number | null
  video_url: string
}

function App() {
  const [searchText, setSearchText] = useState('')
  const [characters, setCharacters] = useState<Character[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (text: string) => {
    setSearchText(text)
    setError(null)
    if (!text) {
      setCharacters([])
      return
    }

    setLoading(true)
    try {
      console.log('Searching for:', text)
      const { data, error } = await supabase
        .from('characters')
        .select('*')
        .ilike('character', `%${text}%`)
        .limit(10)

      if (error) {
        console.error('Supabase error:', error)
        throw error
      }
      
      console.log('Search results:', data)
      setCharacters(data || [])
    } catch (error: any) {
      console.error('Error fetching characters:', error)
      setError(error.message || '查詢時發生錯誤')
      setCharacters([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          陳國昭老師趙孟頫每日一字教學影片查詢
        </Typography>
        
        <TextField
          fullWidth
          label="請輸入一個中文字查詢影片，目前共收錄 1421 個字"
          variant="outlined"
          value={searchText}
          onChange={(e) => handleSearch(e.target.value)}
          sx={{ mb: 2 }}
        />

        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
          <Link
            href="https://www.facebook.com/groups/1396609563919682"
            target="_blank"
            rel="noopener noreferrer"
            sx={{ 
              textDecoration: 'none', 
              color: 'primary.main',
              mr: 2,
              '&:hover': {
                textDecoration: 'underline'
              }
            }}
          >
            陳國昭老師創作專欄
          </Link>
          <Link
            href="https://readforwriting.art/"
            target="_blank"
            rel="noopener noreferrer"
            sx={{ 
              textDecoration: 'none', 
              color: 'primary.main',
              '&:hover': {
                textDecoration: 'underline'
              }
            }}
          >
            關於開發者
          </Link>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box display="flex" justifyContent="center" my={4}>
            <CircularProgress />
          </Box>
        ) : (
          <Box>
            {characters.length === 0 && searchText && !error ? (
              <Alert severity="info">
                沒有找到符合的字
              </Alert>
            ) : (
              characters.map((char) => (
                <Paper key={char.id} sx={{ p: 2, mb: 2 }}>
                  <Typography variant="h5" gutterBottom>
                    {char.character}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    章節：{char.chapter} | 序號：{char.serial} | 部首：{char.radical || '無'}
                  </Typography>
                  <Box sx={{ mt: 2, position: 'relative', paddingTop: '56.25%' }}>
                    <iframe
                      src={`https://www.youtube.com/embed/${char.video_url.split('v=')[1]}`}
                      style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        border: 0
                      }}
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    />
                  </Box>
                </Paper>
              ))
            )}
          </Box>
        )}
      </Box>
    </Container>
  )
}

export default App
