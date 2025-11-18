# Codebook for Survey on the Effectiveness of Information-Digital Environment in General Secondary Education

This codebook provides descriptions of all variables in the dataset. The original survey was conducted in Ukrainian; variable names and response options are provided here in their original language with English translations.

## Variables

### Demographic Information

#### `Отметка времени` (Timestamp)
- Description: Date and time when the survey response was submitted
- Format: YYYY-MM-DD HH:MM:SS

#### `1. Ваш вік` (Your age)
- Description: Age group of the respondent
- Type: Categorical
- Values:
  - "27-35 років" (27-35 years)
  - "35-45 років" (35-45 years)
  - "45 років і старше" (45 years and older)

#### `2. Ваша стать` (Your gender)
- Description: Gender of the respondent
- Type: Categorical
- Values:
  - "Жіноча" (Female)
  - "Чоловіча" (Male)

#### `3. В якому класі навчається Ваша дитина або Ваші діти (можна обрати кілька варіантів відповідей)?` (In which grade is your child or your children studying? (multiple choices allowed))
- Description: Grade level of the respondent's child/children
- Type: Categorical (multiple choice)
- Values:
  - "1 клас" (1st grade)
  - "2 клас" (2nd grade)
  - "3 клас" (3rd grade)
  - "4 клас" (4th grade)
  - "5 клас" (5th grade)
  - "6 клас" (6th grade)
  - "7 клас" (7th grade)
  - "8 клас" (8th grade)
  - "9 клас" (9th grade)
  - "10 клас" (10th grade)
  - "11 клас" (11th grade)

#### `4. Зазначте свою область проживання` (Indicate your region of residence)
- Description: Region of Ukraine where the respondent lives
- Type: Categorical
- Values: Names of 24 administrative regions of Ukraine and the city of Kyiv

#### `5. У якому населеному пункті розташований Ваш заклад освіти` (In what type of settlement is your educational institution located)
- Description: Type of settlement where the educational institution is located
- Type: Categorical
- Values:
  - "Місто" (City)
  - "Селище міського типу" (Urban-type settlement)
  - "Село" (Village)

### School Information

#### `6. Оберіть тип Вашого закладу освіти` (Select the type of your educational institution)
- Description: Type of educational institution
- Type: Categorical
- Values:
  - "Ліцей" (Lyceum)
  - "Гімназія" (Gymnasium)
  - "Загальноосвітня школа" (General education school)
  - "Заклад загальної середньої освіти" (General secondary education institution)
  - "Навчально-виховний комплекс" (Educational complex)

#### `7. Зазначте форму власності Вашого закладу освіти` (Indicate the ownership form of your educational institution)
- Description: Ownership form of the educational institution
- Type: Categorical
- Values:
  - "Державна" (State/Public)
  - "Приватна" (Private)

#### `8. В якому форматі працює Ваш заклад освіти?` (In what format does your educational institution operate?)
- Description: Educational format during wartime
- Type: Categorical
- Values:
  - "Очний формат" (In-person format)
  - "Дистанційний формат" (Distance learning format)
  - "Змішаний формат" (Mixed format)

#### `9. У скільки змін організовано навчання?` (How many shifts is the learning organized in?)
- Description: Number of shifts in which the educational process is organized
- Type: Categorical
- Values:
  - "В одну зміну" (One shift)
  - "В дві зміни" (Two shifts)

### Digital Environment and Communication

#### `10. Яку освітню платформу або інформаційно-комунікаційну систему використовує Ваш заклад освіти для управління освітнім процесом та комунікації з батьками?` (Which educational platform or information and communication system does your educational institution use for managing the educational process and communicating with parents?)
- Description: Educational platform used by the school
- Type: Categorical
- Values:
  - "Нові знання" (New Knowledge)
  - "Human школа" (Human School)
  - "Мій клас" (My Class)
  - "Єдина школа" (United School)
  - "Моя школа" (My School)
  - "Eddy"
  - "SMART школа" (SMART School)
  - "School Today"
  - "Не знаю" (I don't know)
  - "Інше" (Other)

#### `Якщо зазначили "Інше", то напишіть яку саме систему` (If you selected "Other", please specify which system)
- Description: Open text field for specifying other educational platforms
- Type: Text

#### `11. Які інформаційно-комунікаційні сервіси використовує Ваш заклад освіти для організації навчання в очному чи в змішаному форматі? (можна вибрати декілька варіантів відповідей)` (Which information and communication services does your educational institution use for organizing education in face-to-face or mixed format? (multiple choices allowed))
- Description: Digital services used for learning
- Type: Categorical (multiple choice)
- Values:
  - "Zoom"
  - "Google classroom"
  - "Office 365"
  - "Moodle"
  - "Skype"
  - "Prosvita"
  - "Не знаю" (I don't know)
  - "Інше" (Other)

#### `Якщо зазначили "Інше", то напишіть який саме сервіс` (If you selected "Other", please specify which service)
- Description: Open text field for specifying other digital services
- Type: Text

#### `12. Чи задоволені ви технічною підтримкою (допомогою в разі технічних проблем), яку надає заклад освіти для використання освітньої платформи?` (Are you satisfied with the technical support (help in case of technical problems) provided by the educational institution for using the educational platform?)
- Description: Satisfaction with technical support
- Type: Categorical
- Values:
  - "Так" (Yes)
  - "Частково" (Partially)
  - "Ні, така підтримка не надається" (No, such support is not provided)

#### `13. Чи маєте Ви доступ до електронного журналу та щоденника?` (Do you have access to the electronic journal and diary?)
- Description: Access to electronic student records
- Type: Categorical
- Values:
  - "Так" (Yes)
  - "Ні" (No)

#### `14. Чи сайт Вашого закладу освіти містить актуальну та корисну для батьків інформацію?` (Does your educational institution's website contain relevant and useful information for parents?)
- Description: Usefulness of the school website
- Type: Categorical
- Values:
  - "Так" (Yes)
  - "Частково" (Partially)
  - "Ні" (No)
  - "Сайт не працює" (The website is not working)

#### `15. Зазначте позиції, які містить сайт Вашого закладу освіти (можна вибрати декілька варіантів відповідей)` (Specify the items contained on your educational institution's website (multiple choices allowed))
- Description: Content available on the school website
- Type: Categorical (multiple choice)
- Values:
  - "Посилання на електронні підручники та навчальні матеріали" (Links to electronic textbooks and educational materials)
  - "Поради щодо психологічної підтримки дітей" (Advice on psychological support for children)
  - "Правила безпечного користування інтернетом" (Rules for safe internet use)
  - "Правила поведінки під час онлайн-занять" (Rules of behavior during online classes)
  - "Інструкції або відеоінструкції щодо використання освітньої платформи" (Instructions or video instructions on using the educational platform)
  - "Дотримання принципів академічної доброчесності в освітньому процесі та критерії оцінювання результатів навчання учнів" (Adherence to the principles of academic integrity in the educational process and criteria for evaluating student learning outcomes)
  - "Зворотній зв'язок" (Feedback)
  - "Нічого з вищезазначеного" (None of the above)

#### `16. За допомогою яких комунікаційних сервісів або соціальних мереж Ви спілкуєтесь з класним керівником Вашої дитини? (можна вибрати декілька варіантів відповідей)` (Through which communication services or social networks do you communicate with your child's class teacher? (multiple choices allowed))
- Description: Communication channels with teachers
- Type: Categorical (multiple choice)
- Values:
  - "Viber"
  - "Telegram"
  - "WhatsApp"
  - "Signal"
  - "Месенджер у Facebook" (Facebook Messenger)
  - "Instagram"
  - "Tik-Tok"
  - "Інше" (Other)

#### `Якщо зазначили "Інше", то напишіть що саме використовуєте` (If you selected "Other", please specify what you use)
- Description: Open text field for specifying other communication channels
- Type: Text

#### `17. Чи налагоджений зворотній зв'язок з іншими вчителями?` (Is feedback established with other teachers?)
- Description: Feedback with subject teachers
- Type: Categorical
- Values:
  - "Так" (Yes)
  - "Частково" (Partially)
  - "Ні" (No)

#### `18. Чи практикує Ваш заклад освіти опитування батьків щодо якості організації освітнього процесу?` (Does your educational institution practice surveying parents about the quality of the educational process organization?)
- Description: Parent surveys by the school
- Type: Categorical
- Values:
  - "Так" (Yes)
  - "Ні" (No)

### Child's Digital Skills and Resources

#### `19. Чи має Ваша дитина належні навички для самостійного використання цифрових ресурсів у навчанні?` (Does your child have appropriate skills for independent use of digital resources in learning?)
- Description: Child's digital skills
- Type: Categorical
- Values:
  - "Так" (Yes)
  - "Частково" (Partially)
  - "Ні" (No)

#### `20. Наскільки самостійно навчається Ваша дитина під час дистанційного та змішаного формату навчання?` (How independently does your child learn during distance and mixed learning formats?)
- Description: Child's learning independence
- Type: Categorical
- Values:
  - "Самостійно" (Independently)
  - "Самостійно, але батьки контролюють процес" (Independently, but parents control the process)
  - "Вчиться тільки з підтримкою батьків" (Studies only with parental support)
  - "Займається з репетиторами додатково" (Works with tutors additionally)

#### `21. Чи має Ваша дитина доступ до пристрою (комп'ютера, планшета) для навчання вдома?` (Does your child have access to a device (computer, tablet) for learning at home?)
- Description: Access to digital devices for learning
- Type: Categorical
- Values:
  - "Так" (Yes)
  - "Частково (пристрій доступний не завжди)" (Partially (the device is not always available))
  - "Ні" (No)

#### `22. Що, на Вашу думку, можна покращити в інформаційно-цифровому середовищі Вашого закладу освіти? (опишіть, будь ласка, Ваші пропозиції)` (What, in your opinion, can be improved in the information and digital environment of your educational institution? (please describe your suggestions))
- Description: Open suggestions for improvement
- Type: Text
