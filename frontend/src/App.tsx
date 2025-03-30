import { useState } from 'react'
import { 
  Container, 
  TextField, 
  Box, 
  Typography, 
  Paper,
  CircularProgress,
  Alert,
  Link,
  ToggleButton,
  ToggleButtonGroup,
  Button,
  Grid
} from '@mui/material'
import { supabase } from './lib/supabase'

interface Radical {
  char: string
  number: number
  strokes: number
}

interface Character {
  id: number
  chapter: number
  serial: number
  character: string
  radical: number | null
  video_url: string
}

type SearchMode = 'character' | 'radical'

// 靜態部首資料
const RADICAL_MAP: Record<string, Radical> = {
  "一": { char: "一", number: 1, strokes: 1 },
  "丨": { char: "丨", number: 2, strokes: 1 },
  "丶": { char: "丶", number: 3, strokes: 1 },
  "丿": { char: "丿", number: 4, strokes: 1 },
  "乙": { char: "乙", number: 5, strokes: 1 },
  "亅": { char: "亅", number: 6, strokes: 1 },
  "二": { char: "二", number: 7, strokes: 2 },
  "亠": { char: "亠", number: 8, strokes: 2 },
  "人": { char: "人", number: 9, strokes: 2 },
  "儿": { char: "儿", number: 10, strokes: 2 },
  "入": { char: "入", number: 11, strokes: 2 },
  "八": { char: "八", number: 12, strokes: 2 },
  "冂": { char: "冂", number: 13, strokes: 2 },
  "冖": { char: "冖", number: 14, strokes: 2 },
  "冫": { char: "冫", number: 15, strokes: 2 },
  "几": { char: "几", number: 16, strokes: 2 },
  "凵": { char: "凵", number: 17, strokes: 2 },
  "刀": { char: "刀", number: 18, strokes: 2 },
  "力": { char: "力", number: 19, strokes: 2 },
  "勹": { char: "勹", number: 20, strokes: 2 },
  "匕": { char: "匕", number: 21, strokes: 2 },
  "匚": { char: "匚", number: 22, strokes: 2 },
  "匸": { char: "匸", number: 23, strokes: 2 },
  "十": { char: "十", number: 24, strokes: 2 },
  "卜": { char: "卜", number: 25, strokes: 2 },
  "卩": { char: "卩", number: 26, strokes: 2 },
  "厂": { char: "厂", number: 27, strokes: 2 },
  "厶": { char: "厶", number: 28, strokes: 2 },
  "又": { char: "又", number: 29, strokes: 2 },
  "口": { char: "口", number: 30, strokes: 3 },
  "囗": { char: "囗", number: 31, strokes: 3 },
  "土": { char: "土", number: 32, strokes: 3 },
  "士": { char: "士", number: 33, strokes: 3 },
  "夂": { char: "夂", number: 34, strokes: 3 },
  "夊": { char: "夊", number: 35, strokes: 3 },
  "夕": { char: "夕", number: 36, strokes: 3 },
  "大": { char: "大", number: 37, strokes: 3 },
  "女": { char: "女", number: 38, strokes: 3 },
  "子": { char: "子", number: 39, strokes: 3 },
  "宀": { char: "宀", number: 40, strokes: 3 },
  "寸": { char: "寸", number: 41, strokes: 3 },
  "小": { char: "小", number: 42, strokes: 3 },
  "尢": { char: "尢", number: 43, strokes: 3 },
  "尸": { char: "尸", number: 44, strokes: 3 },
  "屮": { char: "屮", number: 45, strokes: 3 },
  "山": { char: "山", number: 46, strokes: 3 },
  "巛": { char: "巛", number: 47, strokes: 3 },
  "工": { char: "工", number: 48, strokes: 3 },
  "己": { char: "己", number: 49, strokes: 3 },
  "巾": { char: "巾", number: 50, strokes: 3 },
  "干": { char: "干", number: 51, strokes: 3 },
  "幺": { char: "幺", number: 52, strokes: 3 },
  "广": { char: "广", number: 53, strokes: 3 },
  "廴": { char: "廴", number: 54, strokes: 3 },
  "廾": { char: "廾", number: 55, strokes: 3 },
  "弋": { char: "弋", number: 56, strokes: 3 },
  "弓": { char: "弓", number: 57, strokes: 3 },
  "彐": { char: "彐", number: 58, strokes: 3 },
  "彡": { char: "彡", number: 59, strokes: 3 },
  "彳": { char: "彳", number: 60, strokes: 3 },
  "心": { char: "心", number: 61, strokes: 4 },
  "戈": { char: "戈", number: 62, strokes: 4 },
  "戶": { char: "戶", number: 63, strokes: 4 },
  "手": { char: "手", number: 64, strokes: 4 },
  "支": { char: "支", number: 65, strokes: 4 },
  "攴": { char: "攴", number: 66, strokes: 4 },
  "文": { char: "文", number: 67, strokes: 4 },
  "斗": { char: "斗", number: 68, strokes: 4 },
  "斤": { char: "斤", number: 69, strokes: 4 },
  "方": { char: "方", number: 70, strokes: 4 },
  "无": { char: "无", number: 71, strokes: 4 },
  "日": { char: "日", number: 72, strokes: 4 },
  "曰": { char: "曰", number: 73, strokes: 4 },
  "月": { char: "月", number: 74, strokes: 4 },
  "木": { char: "木", number: 75, strokes: 4 },
  "欠": { char: "欠", number: 76, strokes: 4 },
  "止": { char: "止", number: 77, strokes: 4 },
  "歹": { char: "歹", number: 78, strokes: 4 },
  "殳": { char: "殳", number: 79, strokes: 4 },
  "毋": { char: "毋", number: 80, strokes: 4 },
  "比": { char: "比", number: 81, strokes: 4 },
  "毛": { char: "毛", number: 82, strokes: 4 },
  "氏": { char: "氏", number: 83, strokes: 4 },
  "气": { char: "气", number: 84, strokes: 4 },
  "水": { char: "水", number: 85, strokes: 4 },
  "火": { char: "火", number: 86, strokes: 4 },
  "爪": { char: "爪", number: 87, strokes: 4 },
  "父": { char: "父", number: 88, strokes: 4 },
  "爻": { char: "爻", number: 89, strokes: 4 },
  "爿": { char: "爿", number: 90, strokes: 4 },
  "片": { char: "片", number: 91, strokes: 4 },
  "牙": { char: "牙", number: 92, strokes: 4 },
  "牛": { char: "牛", number: 93, strokes: 4 },
  "犬": { char: "犬", number: 94, strokes: 4 },
  "玄": { char: "玄", number: 95, strokes: 5 },
  "玉": { char: "玉", number: 96, strokes: 5 },
  "瓜": { char: "瓜", number: 97, strokes: 5 },
  "瓦": { char: "瓦", number: 98, strokes: 5 },
  "甘": { char: "甘", number: 99, strokes: 5 },
  "生": { char: "生", number: 100, strokes: 5 },
  "用": { char: "用", number: 101, strokes: 5 },
  "田": { char: "田", number: 102, strokes: 5 },
  "疋": { char: "疋", number: 103, strokes: 5 },
  "疒": { char: "疒", number: 104, strokes: 5 },
  "癶": { char: "癶", number: 105, strokes: 5 },
  "白": { char: "白", number: 106, strokes: 5 },
  "皮": { char: "皮", number: 107, strokes: 5 },
  "皿": { char: "皿", number: 108, strokes: 5 },
  "目": { char: "目", number: 109, strokes: 5 },
  "矛": { char: "矛", number: 110, strokes: 5 },
  "矢": { char: "矢", number: 111, strokes: 5 },
  "石": { char: "石", number: 112, strokes: 5 },
  "示": { char: "示", number: 113, strokes: 5 },
  "禸": { char: "禸", number: 114, strokes: 5 },
  "禾": { char: "禾", number: 115, strokes: 5 },
  "穴": { char: "穴", number: 116, strokes: 5 },
  "立": { char: "立", number: 117, strokes: 5 },
  "竹": { char: "竹", number: 118, strokes: 6 },
  "米": { char: "米", number: 119, strokes: 6 },
  "糸": { char: "糸", number: 120, strokes: 6 },
  "缶": { char: "缶", number: 121, strokes: 6 },
  "网": { char: "网", number: 122, strokes: 6 },
  "羊": { char: "羊", number: 123, strokes: 6 },
  "羽": { char: "羽", number: 124, strokes: 6 },
  "老": { char: "老", number: 125, strokes: 6 },
  "而": { char: "而", number: 126, strokes: 6 },
  "耒": { char: "耒", number: 127, strokes: 6 },
  "耳": { char: "耳", number: 128, strokes: 6 },
  "聿": { char: "聿", number: 129, strokes: 6 },
  "肉": { char: "肉", number: 130, strokes: 6 },
  "臣": { char: "臣", number: 131, strokes: 6 },
  "自": { char: "自", number: 132, strokes: 6 },
  "至": { char: "至", number: 133, strokes: 6 },
  "臼": { char: "臼", number: 134, strokes: 6 },
  "舌": { char: "舌", number: 135, strokes: 6 },
  "舛": { char: "舛", number: 136, strokes: 6 },
  "舟": { char: "舟", number: 137, strokes: 6 },
  "艮": { char: "艮", number: 138, strokes: 6 },
  "色": { char: "色", number: 139, strokes: 6 },
  "艸": { char: "艸", number: 140, strokes: 6 },
  "虍": { char: "虍", number: 141, strokes: 6 },
  "虫": { char: "虫", number: 142, strokes: 6 },
  "血": { char: "血", number: 143, strokes: 6 },
  "行": { char: "行", number: 144, strokes: 6 },
  "衣": { char: "衣", number: 145, strokes: 6 },
  "襾": { char: "襾", number: 146, strokes: 6 },
  "見": { char: "見", number: 147, strokes: 7 },
  "角": { char: "角", number: 148, strokes: 7 },
  "言": { char: "言", number: 149, strokes: 7 },
  "谷": { char: "谷", number: 150, strokes: 7 },
  "豆": { char: "豆", number: 151, strokes: 7 },
  "豕": { char: "豕", number: 152, strokes: 7 },
  "豸": { char: "豸", number: 153, strokes: 7 },
  "貝": { char: "貝", number: 154, strokes: 7 },
  "赤": { char: "赤", number: 155, strokes: 7 },
  "走": { char: "走", number: 156, strokes: 7 },
  "足": { char: "足", number: 157, strokes: 7 },
  "身": { char: "身", number: 158, strokes: 7 },
  "車": { char: "車", number: 159, strokes: 7 },
  "辛": { char: "辛", number: 160, strokes: 7 },
  "辰": { char: "辰", number: 161, strokes: 7 },
  "辵": { char: "辵", number: 162, strokes: 7 },
  "邑": { char: "邑", number: 163, strokes: 7 },
  "酉": { char: "酉", number: 164, strokes: 7 },
  "釆": { char: "釆", number: 165, strokes: 7 },
  "里": { char: "里", number: 166, strokes: 7 },
  "金": { char: "金", number: 167, strokes: 8 },
  "長": { char: "長", number: 168, strokes: 8 },
  "門": { char: "門", number: 169, strokes: 8 },
  "阜": { char: "阜", number: 170, strokes: 8 },
  "隶": { char: "隶", number: 171, strokes: 8 },
  "隹": { char: "隹", number: 172, strokes: 8 },
  "雨": { char: "雨", number: 173, strokes: 8 },
  "靑": { char: "靑", number: 174, strokes: 8 },
  "非": { char: "非", number: 175, strokes: 8 },
  "面": { char: "面", number: 176, strokes: 9 },
  "革": { char: "革", number: 177, strokes: 9 },
  "韋": { char: "韋", number: 178, strokes: 9 },
  "韭": { char: "韭", number: 179, strokes: 9 },
  "音": { char: "音", number: 180, strokes: 9 },
  "頁": { char: "頁", number: 181, strokes: 9 },
  "風": { char: "風", number: 182, strokes: 9 },
  "飛": { char: "飛", number: 183, strokes: 9 },
  "食": { char: "食", number: 184, strokes: 9 },
  "首": { char: "首", number: 185, strokes: 9 },
  "香": { char: "香", number: 186, strokes: 9 },
  "馬": { char: "馬", number: 187, strokes: 10 },
  "骨": { char: "骨", number: 188, strokes: 10 },
  "高": { char: "高", number: 189, strokes: 10 },
  "髟": { char: "髟", number: 190, strokes: 10 },
  "鬥": { char: "鬥", number: 191, strokes: 10 },
  "鬯": { char: "鬯", number: 192, strokes: 10 },
  "鬲": { char: "鬲", number: 193, strokes: 10 },
  "鬼": { char: "鬼", number: 194, strokes: 10 },
  "魚": { char: "魚", number: 195, strokes: 11 },
  "鳥": { char: "鳥", number: 196, strokes: 11 },
  "鹵": { char: "鹵", number: 197, strokes: 11 },
  "鹿": { char: "鹿", number: 198, strokes: 11 },
  "麥": { char: "麥", number: 199, strokes: 11 },
  "麻": { char: "麻", number: 200, strokes: 11 },
  "黃": { char: "黃", number: 201, strokes: 12 },
  "黍": { char: "黍", number: 202, strokes: 12 },
  "黑": { char: "黑", number: 203, strokes: 12 },
  "黹": { char: "黹", number: 204, strokes: 12 },
  "黽": { char: "黽", number: 205, strokes: 13 },
  "鼎": { char: "鼎", number: 206, strokes: 13 },
  "鼓": { char: "鼓", number: 207, strokes: 13 },
  "鼠": { char: "鼠", number: 208, strokes: 13 },
  "鼻": { char: "鼻", number: 209, strokes: 14 },
  "齊": { char: "齊", number: 210, strokes: 14 },
  "齒": { char: "齒", number: 211, strokes: 15 },
  "龍": { char: "龍", number: 212, strokes: 16 },
  "龜": { char: "龜", number: 213, strokes: 16 },
  "龠": { char: "龠", number: 214, strokes: 17 }
}

function App() {
  const [searchMode, setSearchMode] = useState<SearchMode>('character')
  const [searchText, setSearchText] = useState('')
  const [strokeCount, setStrokeCount] = useState<number | null>(null)
  const [selectedRadical, setSelectedRadical] = useState<Radical | null>(null)
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

  const handleStrokeCountChange = (count: number) => {
    setStrokeCount(count)
    setError(null)
    setSelectedRadical(null)
    setCharacters([])
  }

  const handleRadicalSelect = async (radical: Radical) => {
    setSelectedRadical(radical)
    setError(null)
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('characters')
        .select('*')
        .eq('radical', radical.number)
        .limit(10)

      if (error) {
        console.error('Supabase error:', error)
        throw error
      }

      setCharacters(data || [])
    } catch (error: any) {
      console.error('Error fetching characters:', error)
      setError(error.message || '查詢時發生錯誤')
      setCharacters([])
    } finally {
      setLoading(false)
    }
  }

  const handleSearchModeChange = (
    event: React.MouseEvent<HTMLElement>,
    newMode: SearchMode | null,
  ) => {
    if (newMode !== null) {
      setSearchMode(newMode)
      setSearchText('')
      setStrokeCount(null)
      setSelectedRadical(null)
      setCharacters([])
    }
  }

  // 根據筆劃數獲取部首列表
  const getRadicalsByStrokeCount = (count: number): Radical[] => {
    return Object.values(RADICAL_MAP).filter(radical => radical.strokes === count)
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          陳國昭老師趙孟頫每日一字教學影片查詢
        </Typography>
        
        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
            <ToggleButtonGroup
              value={searchMode}
              exclusive
              onChange={handleSearchModeChange}
              aria-label="搜尋模式"
            >
              <ToggleButton value="character" aria-label="字元搜尋">
                字元搜尋
              </ToggleButton>
              <ToggleButton value="radical" aria-label="部首搜尋">
                部首搜尋
              </ToggleButton>
            </ToggleButtonGroup>
          </Box>

          {searchMode === 'character' ? (
            <TextField
              fullWidth
              label="請輸入一個中文字查詢影片，目前共收錄 1421 個字"
              variant="outlined"
              value={searchText}
              onChange={(e) => handleSearch(e.target.value)}
            />
          ) : (
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="subtitle1" gutterBottom>
                請選擇部首筆劃數：
              </Typography>
              <Grid 
                container 
                spacing={1} 
                sx={{ 
                  mb: 2,
                  justifyContent: 'center',
                  maxWidth: '100%',
                  margin: '0 auto'
                }}
              >
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17].map((count) => (
                  <Grid item key={count}>
                    <Button
                      variant={strokeCount === count ? "contained" : "outlined"}
                      onClick={() => handleStrokeCountChange(count)}
                      sx={{ minWidth: '48px' }}
                    >
                      {count}劃
                    </Button>
                  </Grid>
                ))}
              </Grid>

              {strokeCount && (
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    請選擇部首：
                  </Typography>
                  <Grid 
                    container 
                    spacing={1} 
                    sx={{ 
                      justifyContent: 'center',
                      maxWidth: '100%',
                      margin: '0 auto'
                    }}
                  >
                    {getRadicalsByStrokeCount(strokeCount).map((radical) => (
                      <Grid item key={radical.number}>
                        <Button
                          variant={selectedRadical?.number === radical.number ? "contained" : "outlined"}
                          onClick={() => handleRadicalSelect(radical)}
                          sx={{ minWidth: '48px' }}
                        >
                          {radical.char}
                        </Button>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              )}
            </Box>
          )}
        </Box>

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
            {characters.length === 0 && ((searchText && searchMode === 'character') || (selectedRadical && searchMode === 'radical')) && !error ? (
              <Alert severity="info">
                沒有找到符合的字
              </Alert>
            ) : characters.length > 0 ? (
              <>
                <Alert severity="success" sx={{ mb: 2 }}>
                  {searchMode === 'character' 
                    ? `找到 ${characters.length} 個包含「${searchText}」的字`
                    : `找到 ${characters.length} 個部首為「${selectedRadical?.char}」的字`
                  }
                </Alert>
                {characters.map((char) => (
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
                ))}
              </>
            ) : null}
          </Box>
        )}
      </Box>
    </Container>
  )
}

export default App
