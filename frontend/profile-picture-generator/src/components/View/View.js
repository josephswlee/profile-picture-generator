import Card from "../Card/Card"
export default function View() {
    return (
        <div className="mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mx-auto grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-8">
        
        <div className="h-32 rounded-lg bg-gray-100">
            <Card></Card>
        </div>
        <div className="h-32 rounded-lg bg-gray-100">
            <Card></Card>
        </div>
        </div>
        </div>
    )
}