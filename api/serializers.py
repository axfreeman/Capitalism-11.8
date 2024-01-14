from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from economy.models import (
    Commodity,
    Simulation,
    Stock,
    Industry,
    SocialClass,
    Owner,
    Trace
)

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = "__all__"

class StockSerializer(serializers.ModelSerializer):
    commodity=ReadOnlyField(source="commodity.name")
    class Meta:
        model = Stock
        fields = [
            "id",
            "owner",
            "usage_type",
            "size",
            "requirement",
            "simulation",
            "commodity",
            "demand",
        ]

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = [
            "id",
            "name",
            "commodity",
        ]

class IndustrySerializer(serializers.ModelSerializer):
    output = ReadOnlyField(source="commodity.name")
    stocks=StockSerializer(many=True,read_only=True)

    class Meta:
        model = Industry
        fields = [
            "id",
            "name",
            "simulation",
            "output",
            "output_scale",
            "output_growth_rate",
            "initial_capital",
            "work_in_progress",
            "current_capital",
            "profit",
            "profit_rate",
            "stocks",
        ]

class SocialClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialClass
        fields = [
            "id",
            "simulation",
            "name",
            "population",
            "participation_ratio",
            "consumption_ratio",
            "revenue",
            "assets",
        ]

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = [
            "id",
            "simulation" ,
            "name",
            "origin",
            "usage",
            "size",
            "total_value",
            "total_price",
            "unit_value",
            "unit_price" ,
            "turnover_time" ,
            "demand" ,
            "supply" ,
            "allocation_ratio" ,
            "display_order" ,
            "image_name" ,
            "tooltip" ,
            "monetarily_effective_demand",
            "investment_proportion",
        ]

class TraceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trace
        fields="__all__"
