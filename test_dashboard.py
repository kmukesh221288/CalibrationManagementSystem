from services.dashboard_service import DashboardService

service = DashboardService()

data = service.get_dashboard_data()

print()

print("Dashboard Summary")

print("---------------------")

print(f"Machines     : {data['machines']}")

print(f"Instruments  : {data['instruments']}")

print(f"History      : {data['history']}")

service.close()