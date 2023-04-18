from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
import random
import string
import sys



def generateGrid(words):

    # Create a blank grid of letters
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]

    # Insert the words into the grid randomly
    for word in words:
        placed = False
        attempts = 0
        while not placed:
            # Choose a random starting position and direction for the word
                start_row = random.randint(0, rows-1)
                start_col = random.randint(0, cols-1)
                direction = random.choice([(1,0), (0,-1), (-1,0), (0,1), (1,1), (-1,1), (1,-1), (-1,-1)])

                end_row = start_row + direction[0] * (len(word)-1)
                end_col = start_col + direction[1] * (len(word)-1)

                # Check if the word fits in the grid in the chosen direction
                if end_row < 0 or end_row >= rows or end_col < 0 or end_col >= cols:
                    if attempts > 500:
                        raise Exception('Not enough room to place ' + word + ' in the grid')
                    attempts+=1
                    continue
                fits = True
                for k in range(len(word)):
                    row = start_row + direction[0] * k
                    col = start_col + direction[1] * k
                    if grid[row][col] != ' ' and grid[row][col] != word[k]:
                        fits = False
                        break
                if fits:
                    # Insert the word into the grid
                    for k in range(len(word)):
                        row = start_row + direction[0] * k
                        col = start_col + direction[1] * k
                        grid[row][col] = word[k]
                    placed = True

    # # # Fill in the remaining grid with random letters
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(string.ascii_lowercase)

    return grid


# # Print the completed word search
# for i in range(rows):
#     print(' '.join(grid[i]))

# # Print the list of words to find
# print('\nWords to Find:')
# for word in words:
#     print(word)
   
def createPage(grid, pdf_file, words, border_thickness, grid_thickness, num_of_trim_lines, line_pattern, current_page):
    if (line_pattern == 'dashed'):
        pdf_file.setDash(6, 3)  #set dash pattern to a 6-point dash followed by a 3-point gap
    elif (line_pattern == 'solid'):
        pdf_file.setDash()
    else:
        raise Exception('Line pattern must be either "dashed" or "solid"')

    
    registerFont(TTFont('Arial', 'Arial.ttf'))
    registerFont(TTFont('Arial-Bold', 'ArialBd.ttf'))

    #draw border around the page with margin of 15
    margin = 15
    padding = 15

    pdf_file.setLineWidth(border_thickness)
    pdf_file.rect(margin, margin, PAGE_WIDTH-(margin * 2), PAGE_HEIGHT- (margin * 2), stroke=1 , fill=0)
    #pdf_file.roundRect(margin, margin, PAGE_WIDTH-(margin * 2), PAGE_HEIGHT- (margin * 2), 10, stroke=1, fill=0)


    #add title
    pdf_file.setFont("Arial-Bold", 20)
    # pdf_file.drawCentredString(PAGE_WIDTH/2 , (PAGE_HEIGHT - (margin * 2) - 10) , "Title")
    pdf_file.drawCentredString(PAGE_WIDTH/2 , (PAGE_HEIGHT - (margin * 2) - 10) , "Word Search")

    #add page number
    pdf_file.setFont("Arial", 10)
    pdf_file.drawCentredString(PAGE_WIDTH/2, 5, "Page " + str(current_page))

    # Add the word grid to the PDF file
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            x = LEFT_MARGIN + col * CELL_SIZE
            y = (PAGE_HEIGHT - (margin * 2) - (CELL_SIZE * 3) - 10) - BOTTOM_MARGIN - row * CELL_SIZE

            if (row == 0 and col == len(grid[row])-1):
                gridTop = y + padding - padding/2
                gridRight = x + padding - padding/2
            if (row == len(grid[row])-1 and col == 0):
                gridLeft = x - padding + padding/2
                gridBottom = y - padding  + padding/2

            pdf_file.setFont('Arial', int(0.7 * CELL_SIZE))
            pdf_file.drawString(x, y, grid[row][col])

    #draw a border around the grid
    pdf_file.setLineWidth(grid_thickness)
    if (num_of_trim_lines < 1 or num_of_trim_lines > 3):
        raise Exception('Number of trim lines must be between 1 and 3')
 
    for i in range(num_of_trim_lines):
        pdf_file.rect(gridLeft - (i * 5), gridBottom - (i * 5), (gridRight - gridLeft + CELL_SIZE/2) + (5 * 2 * i) , (gridTop - gridBottom + CELL_SIZE/2) + (2 * 5 * i))

    #add the words to the bottom of the page
    pdf_file.setFont("Arial", 18)

    x = 50
    y = gridBottom - 50
    for word in words:
        # new line
        if (x >= gridRight):
            y = y - 30
            x =  50
        width = pdf_file.stringWidth(word)
        pdf_file.drawString(x , y, word)
        x += width + 15






rows = 15
cols = 15
PAGE_WIDTH, PAGE_HEIGHT = letter
CELL_SIZE = 25
LEFT_MARGIN = PAGE_WIDTH / 2 - (cols * CELL_SIZE) / 2
BOTTOM_MARGIN = PAGE_HEIGHT / 4 - (rows * CELL_SIZE) / 2
gridLeft, gridBottom, gridTop, gridRight = 0, 0,0,0

def main():

    #read args
    if (len(sys.argv) < 3):
        print("Usage: wordsearch.py <words_seperated_by_colons> <page titles_seperated_by_colons>")
        sys.exit(1)

    word_list = sys.argv[1].split(':')
    page_titles = sys.argv[2].split(':')

    words_per_page = 10
    num_of_pages = 1

    current_page = 0
    for w in range(0, len(word_list), words_per_page):
        for i in range(num_of_pages):
            pdf_file = canvas.Canvas(page_titles[current_page] + " - " + str(i+1) + ".pdf", pagesize=letter)
            #generateGrid(words)
            grid = generateGrid(word_list[w:w+words_per_page])
            createPage(grid, pdf_file, word_list[w:w+words_per_page],2, 2, 2, "solid", current_page+1)
            pdf_file.save()
        current_page +=1 







if __name__ == '__main__':
    main()