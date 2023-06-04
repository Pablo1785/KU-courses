from bs4 import BeautifulSoup
from scraper import get_page
# this module is responsible for parsing and extracting information from the html pages

def fixstring(string):
    return string.replace('\n', ' ').replace('\xa0',' ')
def snakecase(string):
    return string.lower().replace(' ', '_')


def get_panel_info(url:str) -> dict:
    """
    This function attempts to grab:
    - Study board
    - Contracting department
    - Contracting faculty
    - Course coordinator
    -- Lecturers"""
    soup = BeautifulSoup(get_page(url), "html.parser")
    panel_bodies = soup.find_all("div", class_="panel-body")

    # Find the one with the most h5's, this is presumably the one we want
    panel_body = max(panel_bodies, key=lambda x: len(x.find_all("h5")))

    # Grabbing top elements
    dl = panel_body.find("dl", class_="dl-horizontal")
    #top_elements = {dt.text: dd.text for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"))} # This is the one that processes schedule
    top_elements = {dt.text: checkdiv(dd) for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"))} # This is the one that processes schedule


    # Grabbing bottom elements
    h5s = panel_body.find_all("h5")
    # For every h5, get the next div
    siblings = [h5.find_next_sibling() for h5 in h5s]

    # if a sibling is a ul, get the li's
    siblings = [s.find_all("li") if s.name == "ul" else s for s in siblings]

    # bottom elements are the 5(?) in the h5s
    def remove_spans(soup):
        """
        Removes all span tags from a soup, used to remove the mailto links
        """
        try:
            for span in soup.find_all("span"):
                span.decompose()
        except AttributeError:
            pass
        return soup

    bottom_elements = {h5.text: [remove_spans(sibling).text.strip() for sibling in siblings[i]] for i, h5 in enumerate(h5s)}
    final_dict = {
        "URL": url,
        **top_elements,
        **bottom_elements,
        "last-modified": panel_body.find("div", class_="last-modified").text}
    
    # Lowercase all keys
    return {k.lower(): v for k, v in final_dict.items()}
    
def get_course_items(url:str) -> dict:
    # Find a div with regex class * main-content
    soup = BeautifulSoup(get_page(url), "html.parser")
    main_content = soup.find("div", class_=lambda x: x and "main-content" in x)
    
    out_dict = {}
    out_dict["primary title"] = main_content.find("h1").text.strip()

    def english_title(soup):
        # If the english title exists, return else return None
        try:
            # it exists in a div with id course-language
            return soup.find("div", id="course-language").text.strip()
        except AttributeError:
            return None
        
    out_dict["english title"] = english_title(main_content)

    out_dict["course content"] = main_content.find("div", id="course-content").text.strip()

    # field is either named course-prerequisites or course-skills
    def grab_prerequisites(soup):
        try:
            return soup.find("div", id="course-skills").text.strip()
        except AttributeError:
            try:
                return soup.find("div", id="course-prerequisites").text.strip()
            except AttributeError:
                return None
        
    out_dict["recommended prerequisites"] = grab_prerequisites(main_content)

    def grab_exam_table(soup):
        exams = soup.find("div", id="course-exams1").find("dl")
        return {dt.text.strip(): dd.text.strip() for dt, dd in zip(exams.find_all("dt"), exams.find_all("dd"))}
    
    out_dict["exams"] =  grab_exam_table(main_content) 


    def grab_course_load(soup):
        course_load = soup.find("div", id="course-load")
        # li's are key-vals and should be zipped
        lis = course_load.find_all("li")
        lis = [li.text.strip() for li in lis]
        # zip every other element
        temp_dict = {k: v for k, v in zip(lis[::2], lis[1::2])}

        return temp_dict

        
    out_dict["course load"] = grab_course_load(main_content)

    return out_dict

def process_course_div(course_soup):
    # find the a tag, this is the name of the section
    key = course_soup.find("a").text.strip()
    # find the div containing the tags
    div = course_soup.find("div")
    # find all the tags
    tags = div.find_all(recursive=False)
    # process
   # print(key)
    value = [process_course_item(tag) for tag in tags]
   # print(value)
    
    # find all text in the div itself
    div_text = div.find_all(text=True, recursive=False)
    
    # append text to value
    value += [" "+text.strip() for text in div_text if text.strip() != ""]

    return {key: value}

def checkdiv(tag):
    divs = tag.find_all('div')
    if divs:
        
        return '__DIV__'.join((d.text or '').strip() for d in divs)
        #return '__DIV__'.join(d.text.strip() for d in divs)
    else:
        return tag.text.strip()
        #return ' '.join(tag.stripped_strings)

def process_course_item(course_soup):
        
    match course_soup.name:
        case "p":
            return course_soup.text.strip()
        case "h5":
            return course_soup.text.strip()
        case "ul":
            return [li.text.strip() for li in course_soup.find_all("li")]
        case "dl":
            return {dt.text.strip(): checkdiv(dd) for dt, dd in zip(course_soup.find_all("dt"), course_soup.find_all("dd"))} # TODO FIX THIS: this calling .text collapses listed structures such as stacks of divs into a single text, 2 exams get merged etc.
        case "a":
            return course_soup.text.strip()
        case "div":
            return course_soup.text.strip()
"""
def process_course_item(course_soup):
    match course_soup.name:
        case "p":
            return course_soup.text.strip()
        case "h5":
            return course_soup.text.strip()
        case "ul":
            return [li.text.strip() for li in course_soup.find_all("li")]
        case "dl":
            return {dt.text.strip(): dd.text.strip() for dt, dd in zip(course_soup.find_all("dt"), course_soup.find_all("dd"))} # TODO FIX THIS: this calling .text collapses listed structures such as stacks of divs into a single text, 2 exams get merged etc.
        case "a":
            return course_soup.text.strip()
        case "div":
            return course_soup.text.strip() + " WARNIGN DIV"
"""

def get_course_items2(url:str) -> dict:
    # Find a div with regex class * main-content
    soup = BeautifulSoup(get_page(url), "html.parser")
    main_content = soup.find("div", class_=lambda x: x and "main-content" in x)
    
    out_dict = {}
    out_dict["primary title"] = main_content.find("h1").text.strip()

    course_items = main_content.find_all("div", class_="course-item")
    

    course_items = [process_course_div(course_item) for course_item in course_items]
    # append every dict to out_dict
    for course_item in course_items:
        out_dict = {**out_dict, **course_item}
    
    
    return out_dict


def rename_examkey(course):
    # Correctly name exam key
    for key in course.keys():
        if (key.startswith('Exam')) or key.startswith('Eksa'):
            examkey = key
            oldexam = course[key]
    del course[examkey]
    course['Exam'] = oldexam
    return course

def rename_exam_subkey(course):
    # Translate exam keys
    dk_en_exam_dict = {
        'Reeksamen': 'Re-exam',
        'Hjælpemidler': 'Aid',
        'Eksamensperiode': 'Exam period',
        'Bedømmelsesform': 'Marking scale',
        'Prøveformsdetaljer': 'Type of assessment details',
        'Prøveform': 'Type of assessment',
        'Krav til indstilling til eksamen': 'Exam registration requirements',
        'Point': 'Credit',
        'Censurform': 'Censorship form',
    }
    if isinstance(course['Exam'], dict):
        keylist = list(course['Exam'].keys())
        for key in keylist:
            if key in dk_en_exam_dict.keys():
                thisvalue = course['Exam'][key]
                del course['Exam'][key]
                course['Exam'][dk_en_exam_dict[key]] = thisvalue
    return course

## Få workload fra en liste med en liste med key value pairs (efter header "category", "hours")
import string 
def dictify_workload(course):
    workdict = {}
    worklist = course['Workload'][0][2:]
    while worklist:
        key = worklist.pop(0)
        value = worklist.pop(0)
        workdict[key]=float(value.replace(",", "."))
    course['Workload'] = workdict
    return course

def translate_workkeys(course):
    workload_dictionary = {'E-læring': 'E-Learning',
        'Eksamen': 'Exam',
        'Laboratorie': 'Laboratory',
        'Studiegrupper': 'Study Groups',
        'Teoretiske øvelser': 'Theory exercises',
        'Feltarbejde': 'Field Work',
        'Forberedelse (anslået)': 'Preparation',
        'Eksamensforberedelse': 'Exam Preparation',
        'Ekskursioner': 'Excursions',
        'Forelæsninger': 'Lectures',
        'Praktiske øvelser': 'Practical exercises',
        'Projektarbejde': 'Project work',
        'Øvelser': 'Exercises',
        'Vejledning': 'Guidance',
        'Holdundervisning': 'Class Instruction',
        'Praktik': 'Practical Training',
        'I alt': 'Total'} # Seminar is Seminar

    keylist = list(course['Workload'].keys())
    for key in keylist:
        if key in workload_dictionary.keys():
            thisvalue = course['Workload'][key]
            del course['Workload'][key]
            course['Workload'][workload_dictionary[key]] = thisvalue
    return course


def fix_primary_title(course):
    course['primary title'] = fixstring(course['primary title'][11:])
    return course

def normalise_language(c):
    # normalize language codes from 
    # {'Dansk', 'Engelsk', 'English', 'English - Partially in Danish'} 
    # to 'en' or 'da'
    l = c['language'].lower()
    if l.startswith('da'):
        c['language'] = 'da'
    elif l.startswith('en'):
        c['language'] = 'en'
    return c

def tidy_content(c):
    def replace_chars(lst):
        while None in lst:
            lst.remove(None)
        while "" in lst:
            lst.remove("")
        for i in range(len(lst)):
            if isinstance(lst[i], list):
                replace_chars(lst[i])
            elif isinstance(lst[i], str):
                lst[i] = fixstring(lst[i])
            else:
                print('undetermined content type', type(lst[i]))
                print(lst[i])
        return lst

    c['Content']=replace_chars(c['Content'])
    c['Learning Outcome'] = replace_chars(c['Learning Outcome'])
    return c

def floatify_credit(c):
    l = c['credit'].lower()
    l = fixstring(l).replace(',','.').replace(' ects', '')
    l = float(l)
    c['credit'] = l
    return c

def get_all_info(url):

    dk_to_en_keys = {'varighed': 'duration',
        'kursuskapacitet': 'course capacity',
        'udbydende institutter': 'contracting departments', #
        'contracting department': 'contracting departments', #
        'udbydende institut': 'contracting departments',    # These map to the same.
        'studienævn': 'study board',
        'kursuskode': 'course code',
        'niveau': 'level',
        'sprog': 'language',
        'Formelle krav': 'Formal requirements',
        'skemagruppe': 'schedule',
        'undervisere': 'lecturers',
        'Anbefalede faglige forudsætninger': 'Recommended Academic Qualifications',
        'Arbejdsbelastning': 'Workload',
        'Feedbackform': 'Feedback form',
        'Bemærkninger': 'Remarks',
        'Kursusindhold': 'Content',
        'Målbeskrivelser': 'Learning Outcome',
        'Undervisningsmateriale': 'Literature',
        'kursusansvarlige': 'course coordinators',
        'Uddannelse': 'Education',
        'placering': 'placement',
        'Undervisningsform': 'Teaching and learning methods',
        'point': 'credit',
        'udbydende fakultet': 'contracting faculty',
        'Tilmelding': 'Sign up'}
    dk_to_en_faculties = {
            'Det Juridiske Fakultet': 'Faculty of Law',
            'Det Humanistiske Fakultet': 'Faculty of Humanities',
            'Det Teologiske Fakultet': 'Faculty of Theology',
            'Det Sundhedsvidenskabelige Fakultet': 'Faculty of Health and Medical Sciences',
            'Det Natur- og Biovidenskabelige Fakultet': 'Faculty of Science',
            'Det Samfundsvidenskabelige Fakultet': 'Faculty of Social Sciences'}
    site = {
        **get_panel_info(url),
        **get_course_items2(url)
    }
    # Translate keys to english
    site = {dk_to_en_keys.get(k, k): v for k, v in site.items()}

    # Translate faculties to english
    faculty = site['contracting faculty'][0]  

    # only attempt to translate if the danish_name is in the translation dictionary
    if faculty in dk_to_en_faculties:
        english_name = dk_to_en_faculties[faculty] 
        site['contracting faculty'] = english_name  
    else:
        site['contracting faculty'] = faculty

    # Only keep the science dept:
    if not site['contracting faculty'] == 'Faculty of Science':
        return None

    pipeline = [
        rename_examkey,
        rename_exam_subkey,
        dictify_workload,
        translate_workkeys,
        fix_primary_title,
        normalise_language,
        tidy_content,
        floatify_credit
    ]

    for func in pipeline:
        site = func(site)
    return site


<<<<<<< HEAD

    return all_info_en


=======
>>>>>>> refs/remotes/origin/main
# THIS IS USED TO DEOBFUSCATE TAGS IN COURSE COORDINATORS
def deobfuscate(s):
    s = s.split('-')
    if len(s) == 1:
        return s
    m = (len(s[1]) // 2) % 4 + 2
    p = ''
    for i in range(0, len(s[1]), 2):
        # convert two hex digits and subtract by m
        value = int(s[1][i:i+2], 16) - m
        p += chr(value)
    return p
