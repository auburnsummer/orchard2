import { Navbar } from "@cafe/components/ui/Navbar"

export function PharmacyNavbar() {
    const links = [
        {
            label: "Pharmacy Tools",
            href: "/pharmacy/"
        },
        {
            label: "Bulk Transfer Levels",
            href: "/pharmacy/bulk-transfer/"
        }
    ]

    return <Navbar links={links} />
}