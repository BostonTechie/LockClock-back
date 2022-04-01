import { useAppContext } from "../global/Session";
const { userHasAuthenticated } = useAppContext(false);

const [isAuthenticated, userHasAuthenticated] = useState(false)